from datetime import datetime
import functools
import json

import click
import pandas as pd
import uvicorn

from yatta.server.dev import SERVER_DEV_PORT, run_frontend_dev, setup_frontend_dev
from yatta.server.plugins import setup_plugins
from yatta.utils import SRC_DIR, link_config_path


@click.group()
def cli():
    pass


def load_config(func):
    @click.option(
        "--config",
        "-c",
        help="Path to the configuration file",
    )
    @click.option(
        "--config_name",
        "-n",
        default="default",
        help="Name of the settings object in the configuration file",
    )
    @functools.wraps(func)
    def wrapper(config, config_name, *args, **kwargs):
        # we create a symlink to an internal config file path so that the server can
        # load from a known path -- this is necessary because we can't pass the path
        # in at runtime.
        # TODO: find a better way to do this
        print("Using config file:", config)
        link_config_path(config)

        # TODO: save and check against dataset hash, and prompt to reassign
        # and/or migrate annotations if different

        # set up plugins
        setup_plugins()

        # we don't import any server code until the config is loaded
        from yatta.server.db import create_db_and_tables
        from yatta.server.settings import settings

        if settings.dataset is None:
            click.echo("No dataset specified in config file")
        elif len(settings.dataset) > 50_000:
            click.echo(
                "Warning: large dataset detected. This may slow down the server."
            )
        create_db_and_tables()

        return func(*args, **kwargs)

    return wrapper


@cli.command()
@load_config
def list_plugins():
    """List available plugins"""
    from yatta.server.plugins import get_plugins

    print(get_plugins())


@cli.command()
@load_config
def dev():
    """Run the development server

    The development server uses the vite dev server and proxies requests to the
    API server.

    The production server flips this, serving the frontend from the API server.
    """
    # check if npm is installed
    if not setup_frontend_dev():
        return

    from yatta.server.settings import settings

    run_frontend_dev(port=settings.port)
    uvicorn.run(
        "yatta.server.app:dev",
        port=SERVER_DEV_PORT,
        reload=True,
        reload_dirs=[str(SRC_DIR)],
    )


@cli.command()
@load_config
def serve():
    """Run the development server

    The development server uses the vite dev server and proxies requests to the
    API server.

    The production server flips this, serving the frontend from the API server.
    """
    from yatta.server.settings import settings

    uvicorn.run(
        "yatta.server.app:app",
        port=settings.port,
        host="0.0.0.0",
    )


@cli.command()
@load_config
@click.argument("--format", type=click.Choice(["csv", "json", "ndjson"]), default="csv")
def dump_annotations(format):
    from sqlmodel import select

    from yatta.server.db import Session, engine
    from yatta.server.models import AnnotationAssignment

    dataframe = []
    with Session(engine) as db:
        annotations = db.exec(select(AnnotationAssignment)).all()
        for annotation in annotations:
            dataframe.append(
                dict(
                    user_id=annotation.user_id,
                    datum_id=annotation.datum_id,
                    is_complete=annotation.is_complete,
                    annotation=json.dumps(annotation.annotation),
                )
            )
    df = pd.DataFrame(dataframe)
    filename = f"{datetime.now().strftime('%Y%m%d-%H%M')}-annotations.{format}"
    if format == "json":
        df.to_json(filename, orient="records")
    elif format == "ndjson":
        df.to_json(filename, orient="records", lines=True)
    else:
        df.to_csv(filename, index=False)


@cli.command()
@load_config
@click.argument("distributor")
@click.option("--exclude_users", "-e", multiple=True, default=[])
def assign(distributor, exclude_users):
    from sqlmodel import select

    from yatta.server.db import Session, engine
    from yatta.server.models import AnnotationAssignment, User
    from yatta.server.settings import settings

    with Session(engine) as db:
        users = db.exec(select(User).where(~User.username.in_(exclude_users))).all()
        distributors = settings.data_distributors
        if distributor not in distributors:
            raise ValueError("Distributor {} not found".format(distributor))
        distributor = distributors[distributor](settings.dataset)
        assignments = list(distributor.assign([user.id for user in users]))
        assignments = [
            AnnotationAssignment(
                user_id=user_id, datum_id=index, is_complete=False, annotation=None
            )
            for user_id, index in assignments
        ]
        db.add_all(assignments)
        db.commit()


@cli.group()
def user():
    pass


@user.command()
@load_config
@click.option("--first_name", required=True, prompt=True)
@click.option("--last_name", required=True, prompt=True)
@click.option("--username", "-u", required=True, prompt=True)
@click.password_option()
def add(first_name, last_name, username, password):
    from yatta.server.auth import add_user
    from yatta.server.db import Session, engine
    from yatta.server.models import UserCreate

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


@user.command(name="list")
@load_config
def list_users():
    from sqlmodel import select

    from yatta.server.db import Session, engine
    from yatta.server.models import User

    with Session(engine) as db:
        users = db.exec(select(User)).all()
        for user in users:
            stats = f" ({user.num_completed}/{user.num_assigned})"
            admin = " (admin)" if user.is_admin else ""
            click.echo(f"{user.id}: {user.username}{stats}{admin}")


@user.command()
@load_config
@click.argument("username")
def make_admin(username):
    from sqlmodel import select

    from yatta.server.db import Session, engine
    from yatta.server.models import User

    with Session(engine) as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise click.ClickException("User not found")
        user.is_admin = True
        db.commit()
        click.echo(f"User {username} is now an admin")
