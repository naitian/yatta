from datetime import timedelta, datetime, timezone
from contextlib import asynccontextmanager
from typing import Union, Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from werkzeug.security import check_password_hash
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


def create_jwt(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def create_token(user: User, expires_delta: timedelta | None = None):
    access_token = create_jwt(
        data={"sub": f"username.{user.username}"},
        expires_delta=expires_delta
        if expires_delta is not None
        else settings.access_timeout,
    )
    return UserToken.model_validate(
        user.model_dump(), update={"access_token": access_token, "token_type": "bearer"}
    )


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


app.mount(
    "/",
    SPAStaticFiles(directory=SRC_DIR / "client" / "dist", html=True),
    name="client",
)
