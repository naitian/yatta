from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from sqlmodel import Session, select

from yatta.server.auth import add_user, create_token
from yatta.server.db import create_db_and_tables, get_session
from yatta.server.models import (
    User,
    UserCreate,
    UserToken,
    AnnotationAssignment,
    AnnotationAssignmentResponse,
)
from yatta.server.dev import SPAStaticFiles
from yatta.server.plugins import get_plugins
from yatta.server.settings import settings
from yatta.utils import SRC_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


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


@app.post("/api/register", response_model=User)
async def create_user(user: UserCreate, session: Annotated[get_session, Depends()]):
    try:
        return add_user(user, session)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")


@app.post("/api/token", response_model=UserToken)
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


@app.post("/api/refresh", response_model=UserToken)
async def refresh(
    user: Annotated[User, Depends(get_current_user)],
):
    token = create_token(user)
    return token


def get_annotation_assignment(user: User, datum_id: str, session: Session):
    annotation_assignment = session.exec(
        select(AnnotationAssignment)
        .where(AnnotationAssignment.user_id == user.id)
        .where(AnnotationAssignment.datum_id == datum_id)
    ).first()
    if not annotation_assignment:
        raise HTTPException(status_code=404, detail="Annotation assignment not found")
    return annotation_assignment


@app.get("/api/annotate/{datum_id}")
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
            "annotation": annotation_assignment.annotation,
            "is_complete": annotation_assignment.is_complete,
        }
    )


@app.post("/api/annotate/{datum_id}")
async def post_annotation(
    datum_id: int,
    user: Annotated[User, Depends(get_current_user)],
    annotation: str,
    session: Annotated[get_session, Depends()],
):
    annotation_assignment = get_annotation_assignment(user, datum_id, session)
    annotation_assignment.annotation = annotation

    try:
        AnnotationAssignment.model_validate(annotation_assignment)
        annotation_assignment.is_complete = True
        session.add(annotation_assignment)
        session.commit()
    except ValidationError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="Invalid annotation: " + str(e))

    return AnnotationAssignmentResponse(
        datum=settings.dataset[datum_id],
        annotation=annotation,
        is_complete=annotation_assignment.is_complete,
    )


@app.get("/api/task")
async def get_task(
    user: Annotated[User, Depends(get_current_user)]
):
    return {
        "task": settings.task,
        "dependencies": [f"{name}.js" for name in get_plugins()]
    }


@app.get("/plugins/{plugin_name}.js")
async def get_plugin(plugin_name: str):
    plugins = get_plugins()
    if plugin_name not in plugins:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return FileResponse(plugins[plugin_name].JS_PATH)

app.mount(
    "/",
    SPAStaticFiles(directory=SRC_DIR / "client" / "dist", html=True),
    name="client",
)
