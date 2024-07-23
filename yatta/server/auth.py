from jose import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash

from yatta.core.db import Session
from yatta.core.models import User, UserCreate, UserToken
from yatta.server.settings import settings


def add_user(user: UserCreate, session: Session):
    hashed_password = generate_password_hash(user.password)
    db_user = User.model_validate(user, update={"hashed_password": hashed_password})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


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