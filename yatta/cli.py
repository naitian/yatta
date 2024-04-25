import functools

import click
import uvicorn

from yatta.server.dev import run_frontend_dev, setup_frontend_dev
from yatta.utils import relative_path, link_config_path


@click.group()
def cli():
    pass


def load_config(func):
    @click.option(
        "--config",
        "-c",
        default=relative_path("config/default.py"),
        help="Path to the configuration file",
    )
    @functools.wraps(func)
    def wrapper(config, *args, **kwargs):
        # we create a symlink to an internal config file path so that the server can
        # load from a known path -- this is necessary because we can't pass the path
        # in at runtime.
        # TODO: find a better way to do this
        link_config_path(config)

        # we use nested imports for any server code to ensure that they run
        # after the config has been established.
        from yatta.server.db import create_db_and_tables
        create_db_and_tables()

        return func(*args, **kwargs)

    return wrapper


@cli.command()
@load_config
def dev():
    """Run the development server"""
    # check if npm is installed
    if not setup_frontend_dev():
        return
    run_frontend_dev()

    from yatta.server.settings import settings

    uvicorn.run("yatta.server.app:app", port=settings.port, reload=True)


@cli.command()
@load_config
@click.argument("distributor")
@click.option("--exclude_users", "-e", multiple=True, default=[])
def assign(distributor, exclude_users):
    from yatta.server.db import Session, engine
    from yatta.server.models import User, AnnotationAssignment
    from yatta.server.settings import settings

    from sqlmodel import select

    with Session(engine) as db:
        users = db.exec(select(User).where(~User.username.in_(exclude_users))).all()
        distributors = settings.data_distributors
        if distributor not in distributors:
            raise ValueError("Distributor {} not found".format(distributor))
        distributor = distributors[distributor](settings.dataset)
        assignments = list(distributor.assign([user for user in users]))
        assignments = [
            AnnotationAssignment(
                user_id=user.id, datum_id=index, is_complete=False, annotation=None
            )
            for user, index in assignments
        ]
        db.add_all(assignments)
        db.commit()


@cli.command()
@load_config
@click.option("--first_name", required=True, prompt=True)
@click.option("--last_name", required=True, prompt=True)
@click.option("--username", "-u", required=True, prompt=True)
@click.password_option()
def add_user(first_name, last_name, username, password):
    from yatta.server.db import Session, engine
    from yatta.server.models import UserCreate
    from yatta.server.auth import add_user

    with Session(engine) as db:
        user = UserCreate(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
        try:
            add_user(user, db)
        except Exception as e:
            raise click.ClickException("Error adding user: {}".format(e))
        click.echo(f"User {username} added successfully!")
