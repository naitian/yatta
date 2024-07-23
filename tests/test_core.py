from pathlib import Path

import pytest

from yatta.core import Yatta
from yatta.core.db import YattaDb
from yatta.core.models import UserCreate


def test_yatta_create_db(tmp_path):
    db = YattaDb(db_path=tmp_path / "test.db")
    db.create_db_and_tables()

    assert Path("test.db").exists()


@pytest.fixture
def dataset():
    return [1, 2, 3, 4, 5]


@pytest.fixture
def app(tmp_path, dataset):
    return Yatta(dataset=dataset, db_path=tmp_path / "test.db")


@pytest.fixture
def naitian_user():
    return UserCreate.model_validate(
        {
            "first_name": "Naitian",
            "last_name": "Zhou",
            "username": "naitian",
            "password": "password",
        }
    )


def test_yatta_get_missing_user(app):
    with app.session():
        with pytest.raises(ValueError, match="User naitian not found."):
            app.get_user("naitian")


def test_yatta_add_user(app, naitian_user):
    with app.session():
        user = app.add_user(naitian_user)
        assert user.username == "naitian"
        assert user.first_name == "Naitian"
        assert user.is_admin is False


def test_yatta_get_user(app, naitian_user):
    with app.session():
        app.add_user(naitian_user)
        user = app.get_user("naitian")

        assert user.username == "naitian"
        assert user.first_name == "Naitian"
        assert user.is_admin is False


def test_yatta_make_admin(app, naitian_user):
    with app.session():
        user = app.add_user(naitian_user)
        app.make_admin(user)

        assert user.is_admin is True


def test_yatta_no_session(app):
    with pytest.raises(RuntimeError, match="No session found."):
        app.get_user("naitian")


def test_yatta_authenticate_user(app, naitian_user):
    with app.session():
        app.add_user(naitian_user)
        user = app.authenticate_user("naitian", "password")

        assert user.username == "naitian"
        assert user.first_name == "Naitian"
        assert user.is_admin is False


def test_yatta_list_users(app, naitian_user):
    with app.session():
        app.add_user(naitian_user)
        users = app.list_users()
        assert isinstance(users, list)
        assert len(users) == 1
        assert users[0].username == "naitian"
