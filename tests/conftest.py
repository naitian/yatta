import json

import pytest

from yatta.core import Yatta
from yatta.core.models import AnnotationObject, UserCreate


@pytest.fixture()
def dataset():
    return [1, 2, 3, 4, 5]


@pytest.fixture()
def app(tmp_path, dataset):
    return Yatta(dataset=dataset, db_path=tmp_path / "test.db")


@pytest.fixture()
def naitian_user():
    return UserCreate.model_validate(
        {
            "first_name": "Naitian",
            "last_name": "Zhou",
            "username": "naitian",
            "password": "password",
        }
    )


@pytest.fixture()
def complete_annotation():
    return AnnotationObject.model_validate(
        {
            "annotation": {"text": "annotation"},
            "is_complete": True,
            "is_skipped": False,
        }
    )


@pytest.fixture()
def skipped_annotation():
    return AnnotationObject.model_validate(
        {
            "annotation": {"text": "annotation"},
            "is_complete": False,
            "is_skipped": True,
        }
    )


@pytest.fixture()
def incomplete_annotation():
    return AnnotationObject.model_validate(
        {
            "annotation": {"text": "annotation"},
            "is_complete": False,
            "is_skipped": False,
        }
    )
