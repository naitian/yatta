from datetime import timedelta, datetime, timezone
from contextlib import asynccontextmanager
from typing import Union, Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from sqlmodel import select

from yatta.server.auth import add_user
from yatta.server.db import create_db_and_tables, get_session
from yatta.server.models import User, UserCreate, UserToken
from yatta.server.dev import SPAStaticFiles
from yatta.server.settings import settings
from yatta.utils import SRC_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


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

        access_token = create_access_token(
            data={"sub": f"username.{user.username}"},
            expires_delta=settings.access_timeout,
        )
        token = UserToken.model_validate(
            user.model_dump(),
            update={"access_token": access_token, "token_type": "bearer"},
        )
        return token
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())


app.mount(
    "/",
    SPAStaticFiles(directory=SRC_DIR / "client" / "dist", html=True),
    name="client",
)
