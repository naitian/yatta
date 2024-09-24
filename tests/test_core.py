from pathlib import Path

import pytest

from yatta.core.db import YattaDb
from yatta.distributor import AllDistributor


def test_yatta_create_db(tmp_path):
    db = YattaDb(db_path=tmp_path / "test.db")
    db.create_db_and_tables()

    assert Path("test.db").exists()


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


def test_yatta_assign_tasks(app, naitian_user):
    with app.session():
        app.add_user(naitian_user)
        app.distributor = AllDistributor
        app.assign_tasks()

        users = app.list_users()
        assert users[0].num_assigned == 5
        assert users[0].num_completed == 0
        assert users[0].num_skipped == 0
        assert users[0].next_assignment == 0


def test_yatta_assign_tasks_inline(app, naitian_user):
    with app.session():
        app.add_user(naitian_user)
        app.assign_tasks(distributor=AllDistributor)

        users = app.list_users()
        assert users[0].num_assigned == 5
        assert users[0].num_completed == 0
        assert users[0].num_skipped == 0
        assert users[0].next_assignment == 0


def test_yatta_assign_tasks_exclude(app, naitian_user):
    with app.session():
        app.add_user(naitian_user)
        user = app.get_user("naitian")
        app.assign_tasks(exclude_users=[user.id], distributor=AllDistributor)

        users = app.list_users()
        assert users[0].num_assigned == 0
        assert users[0].num_completed == 0
        assert users[0].num_skipped == 0
        assert users[0].next_assignment is None


def test_yatta_ordering(app, naitian_user):
    with app.session():
        app.add_user(naitian_user)
        app.assign_tasks(distributor=AllDistributor)
        app.assign_all_orderings(ordering=lambda x: x[::-1])  # reverse ordering

        users = app.list_users()
        assert users[0].num_assigned == 5
        assert users[0].num_completed == 0
        assert users[0].num_skipped == 0
        assert users[0].next_assignment == 4


def test_yatta_get_annotation(app, naitian_user):
    with app.session():
        app.add_user(naitian_user)
        app.assign_tasks(distributor=AllDistributor)
        app.assign_all_orderings(ordering=lambda x: x)  # reverse ordering

        user = app.get_user("naitian")
        assignment = app.get_annotation(user, 4)

        assert assignment.annotation is None
        assert assignment.next is None
        assert assignment.prev == 3


def test_yatta_set_annotation(app, naitian_user, complete_annotation):
    with app.session():
        app.add_user(naitian_user)
        app.assign_tasks(distributor=AllDistributor)
        app.assign_all_orderings(ordering=lambda x: x)  # reverse ordering

        user = app.get_user("naitian")
        assignment = app.get_annotation(user, 4)
        app.set_annotation(user, 4, complete_annotation)

        assignment = app.get_annotation(user, 4)
        assert isinstance(assignment.annotation, dict)
        assert assignment.is_complete is True
        assert assignment.annotation["text"] == "annotation"


def test_yatta_set_skip_annotation(app, naitian_user, skipped_annotation):
    with app.session():
        app.add_user(naitian_user)
        app.assign_tasks(distributor=AllDistributor)
        app.assign_all_orderings(ordering=lambda x: x)  # reverse ordering

        user = app.get_user("naitian")
        assignment = app.get_annotation(user, 4)
        app.set_annotation(user, 4, skipped_annotation)

        assignment = app.get_annotation(user, 4)
        assert isinstance(assignment.annotation, dict)
        assert assignment.is_skipped is True
        assert assignment.annotation["text"] == "annotation"
