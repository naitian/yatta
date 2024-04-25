"""Data models

We put all the data models in the same file to avoid circular imports.
See: https://sqlmodel.tiangolo.com/tutorial/code-structure/#application-file

At some point we might want to split this into separate files for the
~aesthetics~ (readability) but for now this is fine.
"""

from sqlmodel import Field, SQLModel


### User


class UserBase(SQLModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    username: str = Field(unique=True)
    is_admin: None | bool = Field(default=False)


class User(UserBase, table=True):
    """User model for the database."""

    id: int | None = Field(primary_key=True, default=None)
    hashed_password: str = Field(max_length=256)


class UserCreate(UserBase):
    password: str


class UserToken(UserBase):
    access_token: str
    token_type: str = "bearer"


###
