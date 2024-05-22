import itertools
import json
from contextlib import asynccontextmanager
from typing import Annotated

from baize.asgi import Files
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from werkzeug.security import check_password_hash

from yatta.server.auth import add_user, create_token
from yatta.server.db import create_db_and_tables, engine, get_session
from yatta.server.dev import BaizeStaticFiles, SPAStaticFiles
from yatta.server.models import (
    AnnotationAssignment,
    AnnotationAssignmentResponse,
    AnnotationObject,
    User,
    UserCreate,
    UserResponse,
    UserToken,
)
from yatta.server.settings import settings
from yatta.utils import SRC_DIR


def sliding_window(seq, n):
    """Returns a sliding window (of width n) over data from the iterable"""
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def assign_ordering(ordering, assignments, session):
    """Assign an ordering to a list of assignments"""
    for idx, (prev, curr, next) in enumerate(
        sliding_window(itertools.chain([None], ordering(assignments), [None]), 3)
    ):
        curr.rank = idx
        curr.prev = prev.datum_id if prev is not None else None
        curr.next = next.datum_id if next is not None else None
    session.commit()


def assign_all_orderings():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
            assignments = session.exec(
                select(AnnotationAssignment).where(
                    AnnotationAssignment.user_id == user.id
                )
            ).all()
            assign_ordering(settings.ordering, assignments, session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    create_db_and_tables()
    assign_all_orderings()
    yield


app_config = dict(
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
)
app = FastAPI(**app_config)
dev = FastAPI(**app_config)

api = APIRouter()


def get_current_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/token"))],
    session: Annotated[get_session, Depends()],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username = payload.get("sub").removeprefix("username.")
        if not username:
            raise credentials_exception
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


@api.post("/api/register", response_model=User)
async def create_user(user: UserCreate, session: Annotated[get_session, Depends()]):
    try:
        return add_user(user, session)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")


@api.post("/api/token", response_model=UserToken)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[get_session, Depends()],
):
    try:
        user = session.exec(
            select(User).where(User.username == form_data.username)
        ).first()
        if not user or not check_password_hash(
            user.hashed_password, form_data.password
        ):
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        return create_token(user)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())


@api.post("/api/refresh", response_model=UserToken)
async def refresh(
    user: Annotated[User, Depends(get_current_user)],
):
    token = create_token(user)
    return token


@api.get("/api/user", response_model=UserResponse)
async def user_info(
    user: Annotated[User, Depends(get_current_user)],
):
    return user


def get_annotation_assignment(user: User, datum_id: str, session: Session):
    annotation_assignment = session.exec(
        select(AnnotationAssignment)
        .where(AnnotationAssignment.user_id == user.id)
        .where(AnnotationAssignment.datum_id == datum_id)
    ).first()
    if not annotation_assignment:
        raise HTTPException(status_code=404, detail="Annotation assignment not found")
    return annotation_assignment


@api.get("/api/annotate/{datum_id}")
async def get_annotation(
    datum_id: int,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[get_session, Depends()],
):
    annotation_assignment = get_annotation_assignment(user, datum_id, session)
    datum = settings.dataset[datum_id]
    return AnnotationAssignmentResponse(
        **{
            "datum": datum,
            # NOTE: the Json type expects a string, so we serialize the dict
            # this gets converted from a string back into JSON in the response
            # The same happens in the POST request
            "annotation": json.dumps(annotation_assignment.annotation),
            "is_complete": annotation_assignment.is_complete,
            "next": annotation_assignment.next,
            "prev": annotation_assignment.prev,
        }
    )


@api.post("/api/annotate/{datum_id}")
async def post_annotation(
    datum_id: int,
    annotation: AnnotationObject,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[get_session, Depends()],
):
    try:
        annotation_assignment = get_annotation_assignment(user, datum_id, session)
        annotation_assignment.annotation = annotation.annotation
        # only mark as complete if the client says it is
        # otherwise, we assume the client is just saving progress
        annotation_assignment.is_complete = (
            annotation.annotation is not None and annotation.is_complete
        )
        session.commit()
    except ValidationError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="Invalid annotation: " + str(e))

    return AnnotationAssignmentResponse(
        datum=settings.dataset[datum_id],
        annotation=json.dumps(annotation_assignment.annotation),
        is_complete=annotation_assignment.is_complete,
        next=annotation_assignment.next,
        prev=annotation_assignment.prev,
    )


@api.get("/api/task")
async def get_task(user: Annotated[User, Depends(get_current_user)]):
    return {
        "task": settings.task,
        "components": list(aggregate_component_names(settings.task).keys()),
    }


def aggregate_component_names(task):
    """
    task is a dict with keys as the field names and values as the components,
    which have a name attribute

    for now, we ignore components with children; we can add this later

    return a dict component.name -> component
    """
    return {component.name: component for component in task.values()}


@api.get("/api/component/{component_name}")
async def get_plugin_js(component_name: str):
    components = aggregate_component_names(settings.task)
    if component_name not in components:
        raise HTTPException(status_code=404, detail="Component not found")
    return Response(
        content=components[component_name].esm, media_type="application/javascript"
    )


@api.get("/api/css/{component_name}")
async def get_plugin_css(component_name: str):
    components = aggregate_component_names(settings.task)
    if component_name not in components:
        raise HTTPException(status_code=404, detail="Component not found")
    return Response(content=components[component_name].css, media_type="text/css")


def handle(scope, receive, send):
    filepath = scope["path"]
    print(filepath)
    raise HTTPException(404)


for name, path in settings.static_files.items():
    static = FastAPI()
    static.mount("/", BaizeStaticFiles(directory=path, handle_404=handle), name=name)
    app.mount(
        f"/files/{name}/",
        static
    )
    dev.mount(
        f"/files/{name}/",
        static
    )

app.include_router(api)
app.mount(
    "/",
    SPAStaticFiles(directory=SRC_DIR / "client" / "dist", html=True, check_dir=False),
    name="client",
)


dev.include_router(api)
