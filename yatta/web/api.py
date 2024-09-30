import json
from datetime import timedelta
from sqlite3 import IntegrityError
from typing import Any

from pydantic import ValidationError
from quart import Blueprint, Response
from quart.helpers import abort
from quart_auth import AuthUser, current_user, login_required, login_user, logout_user
from quart_schema import validate_request, validate_response

from yatta.core import Yatta
from yatta.core.models import (
    AnnotationAssignment,
    AnnotationAssignmentResponse,
    AnnotationObject,
    ComponentAssignment,
    Login,
    User,
    UserCreate,
    UserResponse,
)


def format_annotation_datum(
    yatta: Yatta, datum: Any, annotation_assignment: AnnotationAssignment
):
    # NOTE: the Json type expects a string, so we serialize the dict
    # this gets converted from a string back into JSON in the response
    # The same happens in the POST request
    # FIXME: move this somewhere else (maybe inside yatta), since it's also in
    # the jupyter widget
    return {
        key: ComponentAssignment(
            datum=component.transform(datum),
            annotation=json.dumps(
                annotation_assignment.annotation[key]
                if annotation_assignment.annotation
                and key in annotation_assignment.annotation
                else None
            ),
        )
        for key, component in yatta.task.items()
    }


def create_api(yatta: Yatta, secret_key: str, access_timeout: timedelta | None = None):
    access_timeout = access_timeout or timedelta(minutes=15)
    api = Blueprint("api", __name__)

    def get_current_user() -> User:
        if current_user.auth_id is None:
            abort(401, "Not authenticated")
        # NOTE: current_user is a Quart-Auth object, not a User object, so we
        # need to get the User object from the database.
        # We can also ignore the type here, since we know that the user is
        # authenticated, so current_user.auth_id cannot be None.
        return yatta.get_user(current_user.auth_id)  # type: ignore

    @api.post("/api/register")
    @validate_request(UserCreate)
    @validate_response(User)
    async def create_user(data: UserCreate) -> User:
        try:
            new_user = yatta.add_user(data)
            return new_user
        except ValidationError as e:
            abort(400, "Invalid user: " + str(e))
        except IntegrityError:
            abort(400, "Username already exists")

    @api.post("/api/login")
    @validate_request(Login)
    @validate_response(User)
    async def login(data: Login) -> User:
        try:
            user = yatta.authenticate_user(data.username, data.password)
            # TODO: we don't subclass User from AuthUser, so we manually do a
            # lookup every time we want user info. This is a little awkward, but
            # I mainly didn't the core models to depend on any of the web stuff.
            # Maybe we can refactor this later such that we have a QuartUser
            # that subclasses AuthUser and User.
            login_user(AuthUser(user.username))
            return user
        except ValueError:
            abort(400, "Incorrect username or password.")
        except Exception as e:
            abort(400, e)

    @api.get("/api/logout")
    @login_required
    async def logout() -> dict:
        logout_user()
        return {"message": "Logged out"}

    # @api.post("/api/refresh", response_model=UserToken)
    # async def refresh(
    #     user: Annotated[User, Depends(get_current_user)],
    # ):
    #     token = create_token(user, secret_key, access_timeout)
    #     return token

    @api.get("/api/user")
    @validate_response(UserResponse)
    @login_required
    async def user_info() -> UserResponse:
        return UserResponse.model_validate(get_current_user())

    # TODO: we ignore the type error here
    # I'm not sure how to fix it -- I suspect it might be a flaw with
    # Quart-Schema (I've filed an issue here:
    # https://github.com/pgjones/quart-schema/issues/91)
    # In the meantime, this should still work, so we will ignore.
    @api.get("/api/annotate/<int:datum_id>")  # type: ignore
    @validate_response(AnnotationAssignmentResponse)
    @login_required
    async def get_annotation(datum_id: int) -> AnnotationAssignmentResponse:
        user = get_current_user()
        annotation_assignment = yatta.get_annotation(user, datum_id)
        datum = yatta.dataset[datum_id]
        response = AnnotationAssignmentResponse(
            components=format_annotation_datum(yatta, datum, annotation_assignment),
            is_complete=annotation_assignment.is_complete,
            is_skipped=annotation_assignment.is_skipped,
            next=annotation_assignment.next,
            prev=annotation_assignment.prev,
        )
        return response

    @api.post("/api/annotate/<int:datum_id>")  # type: ignore
    @validate_request(AnnotationObject)
    @validate_response(AnnotationAssignmentResponse)
    async def post_annotation(
        datum_id: int,
        data: AnnotationObject,
    ) -> AnnotationAssignmentResponse:
        user = get_current_user()
        try:
            annotation_assignment = yatta.set_annotation(user, datum_id, data)
            datum = yatta.dataset[datum_id]
            return AnnotationAssignmentResponse(
                components=format_annotation_datum(yatta, datum, annotation_assignment),
                is_complete=annotation_assignment.is_complete,
                is_skipped=annotation_assignment.is_skipped,
                next=annotation_assignment.next,
                prev=annotation_assignment.prev,
            )
        except ValidationError as e:
            abort(400, "Invalid annotation: " + str(e))

    @api.get("/api/task")
    @login_required
    async def get_task():
        return yatta.get_task()

    @api.get("/api/component/{component_name}")
    async def get_plugin_js(component_name: str):
        components = yatta.get_task()["components"]
        if component_name not in components:
            abort(404, "Component not found")
        return Response(
            response=components[component_name].esm, mimetype="application/javascript"
        )

    @api.get("/api/css/{component_name}")
    async def get_plugin_css(component_name: str):
        components = yatta.get_task()["components"]
        if component_name not in components:
            abort(404, "Component not found")
        return Response(response=components[component_name].css, mimetype="text/css")

    return api
