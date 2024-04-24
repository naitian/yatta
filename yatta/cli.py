import functools

import click
import uvicorn

from yatta.server.dev import run_frontend_dev, setup_frontend_dev
from yatta.utils import relative_path, link_config_path


@click.group()
def cli():
    pass


def server_options(func):
    @click.option(
        "--config",
        "-c",
        default=relative_path("config/default.py"),
        help="Path to the configuration file",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@cli.command()
@server_options
def dev(config):
    """Run the development server"""
    # check if npm is installed
    if not setup_frontend_dev():
        return
    run_frontend_dev()
    # we create a symlink to an internal config file path so that the server can
    # load from a known path -- this is necessary because we can't pass the path
    # in at runtime.
    link_config_path(config)

    from yatta.server.settings import settings

    uvicorn.run("yatta.server.app:app", port=settings.port, reload=True)
