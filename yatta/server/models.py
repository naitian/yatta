"""Data models

We put all the data models in the same file to avoid circular imports.
See: https://sqlmodel.tiangolo.com/tutorial/code-structure/#application-file

At some point we might want to split this into separate files for the
~aesthetics~ (readability) but for now this is fine.
"""

from sqlmodel import Field, SQLModel, Relationship, JSON
from pydantic import computed_field


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
    assignments: list["AnnotationAssignment"] = Relationship(back_populates="user")

    @computed_field
    @property
    def num_completed(self) -> int:
        return len([a for a in self.assignments if a.is_complete])

    @computed_field
    @property
    def num_assigned(self) -> int:
        return len(self.assignments)


class UserCreate(UserBase):
    password: str


class UserToken(UserBase):
    access_token: str
    token_type: str = "bearer"


### Annotations


class AnnotationAssignment(SQLModel, table=True):
    annotation_id: int | None = Field(primary_key=True, default=None)
    datum_id: str = Field()
    is_complete: bool = Field(default=False)
    annotation: str | None = Field(sa_type=JSON, default=None)

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="assignments")
