from werkzeug.security import generate_password_hash

from yatta.core.db import Session
from yatta.core.models import User, UserCreate


def add_user(user: UserCreate, session: Session):
    hashed_password = generate_password_hash(user.password)
    db_user = User.model_validate(user, update={"hashed_password": hashed_password})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

