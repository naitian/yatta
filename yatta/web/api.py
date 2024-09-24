import json
from datetime import timedelta
from sqlite3 import IntegrityError
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError

from yatta.core import Yatta
from yatta.core.models import (
    AnnotationAssignmentResponse,
    AnnotationObject,
    User,
    UserCreate,
    UserResponse,
    UserToken,
)
from yatta.web.auth import create_token


def create_api(yatta: Yatta, secret_key: str, access_timeout: timedelta | None = None):
    access_timeout = access_timeout or timedelta(minutes=15)
    api = APIRouter()

    def get_current_user(
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/token"))],
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            if payload.get("sub") is None:
                raise credentials_exception
            username = str(payload.get("sub")).removeprefix("username.")
            if not username:
                raise credentials_exception
            user = yatta.get_user(username)
            if not user:
                raise credentials_exception
            return user
        except JWTError:
            raise HTTPException(status_code=400, detail="Invalid token")

    @api.post("/api/register", response_model=User)
    async def create_user(user: UserCreate):
        try:
            return yatta.add_user(user)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=e.errors())
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Username already exists")

    @api.post("/api/token", response_model=UserToken)
    async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ):
        try:
            user = yatta.authenticate_user(form_data.username, form_data.password)
            return create_token(user, secret_key, access_timeout)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password."
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)

    @api.post("/api/refresh", response_model=UserToken)
    async def refresh(
        user: Annotated[User, Depends(get_current_user)],
    ):
        token = create_token(user, secret_key, access_timeout)
        return token

    @api.get("/api/user", response_model=UserResponse)
    async def user_info(
        user: Annotated[User, Depends(get_current_user)],
    ):
        return user

    @api.get("/api/annotate/{datum_id}")
    async def get_annotation(
        datum_id: int,
        user: Annotated[User, Depends(get_current_user)],
    ):
        annotation_assignment = yatta.get_annotation(user, datum_id)
        datum = yatta.dataset[datum_id]
        return AnnotationAssignmentResponse(
            **{
                "datum": datum,
                # NOTE: the Json type expects a string, so we serialize the dict
                # this gets converted from a string back into JSON in the response
                # The same happens in the POST request
                "annotation": json.dumps(annotation_assignment.annotation),
                "is_complete": annotation_assignment.is_complete,
                "is_skipped": annotation_assignment.is_skipped,
                "next": annotation_assignment.next,
                "prev": annotation_assignment.prev,
            }
        )

    @api.post("/api/annotate/{datum_id}")
    async def post_annotation(
        datum_id: int,
        annotation: AnnotationObject,
        user: Annotated[User, Depends(get_current_user)],
    ):
        try:
            annotation_assignment = yatta.set_annotation(user, datum_id, annotation)
            return AnnotationAssignmentResponse(
                datum=yatta.dataset[datum_id],
                annotation=json.dumps(annotation_assignment.annotation),
                is_complete=annotation_assignment.is_complete,
                is_skipped=annotation_assignment.is_skipped,
                next=annotation_assignment.next,
                prev=annotation_assignment.prev,
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail="Invalid annotation: " + str(e))

    @api.get("/api/task")
    async def get_task(user: Annotated[User, Depends(get_current_user)]):
        return {
            "task": yatta.task,
            "components": list(aggregate_component_names(yatta.task).keys()),
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
        components = aggregate_component_names(yatta.task)
        if component_name not in components:
            raise HTTPException(status_code=404, detail="Component not found")
        return Response(
            content=components[component_name].esm, media_type="application/javascript"
        )

    @api.get("/api/css/{component_name}")
    async def get_plugin_css(component_name: str):
        components = aggregate_component_names(yatta.task)
        if component_name not in components:
            raise HTTPException(status_code=404, detail="Component not found")
        return Response(content=components[component_name].css, media_type="text/css")

    return api
