"""Data models

We put all the data models in the same file to avoid circular imports.
See: https://sqlmodel.tiangolo.com/tutorial/code-structure/#application-file

At some point we might want to split this into separate files for the
~aesthetics~ (readability) but for now this is fine.
"""

from typing import Optional
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship, JSON
from pydantic import BaseModel, computed_field, Json
import numpy as np


### User


class UserBase(SQLModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    username: str = Field(unique=True)
    is_admin: None | bool = Field(default=False)


class User(UserBase, table=True):
    """User model for the database."""

    id: int = Field(primary_key=True, default=None)
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

    @computed_field
    @property
    def next_assignment(self) -> int | None:
        eligible_assignments = [
            a for a in self.assignments if not a.is_complete and not a.is_skipped
        ]
        if len(eligible_assignments) == 0:
            if len(self.assignments) == 0:
                return None
            return self.assignments[0].datum_id
        min_rank = np.argmin([a.rank for a in eligible_assignments])
        return eligible_assignments[min_rank].datum_id

    @computed_field
    @property
    def num_skipped(self) -> int:
        return len([a for a in self.assignments if a.is_skipped])


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    # TODO: this is a computed field in the database; we replicate it here for
    # the API response
    num_completed: int
    num_skipped: int
    num_assigned: int
    next_assignment: int | None


class UserToken(UserResponse):
    access_token: str
    token_type: str = "bearer"


class Login(BaseModel):
    username: str
    password: str

### Annotations


class AnnotationAssignment(SQLModel, table=True):
    """
    Represents an annotation assignment.

    Attributes:
        annotation_id (int | None): The ID of the annotation (primary key).
        datum_id (int): The ID of the datum.
        is_complete (bool): Indicates if the assignment is complete.
        is_skipped (bool): Indicates if the assignment is skipped.
        annotation (Json | None): The annotation data in JSON format.
        rank (int): The rank of the assignment.
        next (int | None): The datum ID of the next assignment.
        prev (int | None): The datum ID of the previous assignment.
        user_id (int): The ID of the user associated with the assignment.
        user (User): The user associated with the assignment.

    FIXME: is_skipped and is_complete are mutually exclusive. It probably makes
    more sense to have a single field that indicates the status of the
    assignment.
    """

    __table_args__ = (
        UniqueConstraint("datum_id", "user_id", name="unique_assignment"),
    )

    annotation_id: int | None = Field(primary_key=True, default=None)
    datum_id: int = Field()
    is_complete: bool = Field(default=False)
    is_skipped: bool = Field(default=False)
    annotation: Json | None = Field(sa_type=JSON, default=None)
    enabled: bool = Field(default=True)

    rank: int = Field(default=0)
    next: int | None = Field(default=None)
    prev: int | None = Field(default=None)

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="assignments")


# TODO: support more types (e.g., many datasets are potentially nparrays)
# We might want to add a function that normalizes different types of data into
# JSON
class ComponentAssignment(BaseModel):
    datum: Json | dict | int | str
    annotation: Json | None


class AnnotationAssignmentResponse(BaseModel):
    components: dict[str, ComponentAssignment]
    is_complete: bool
    is_skipped: bool
    next: Optional[int] = None
    prev: Optional[int] = None


class AnnotationObject(BaseModel):
    annotation: dict[str, Json] | None
    is_complete: bool = False
    is_skipped: bool = False
