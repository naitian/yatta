import shutil
import click
import uvicorn

from yatta.server.dev import setup_frontend_dev, run_frontend_dev

@click.group()
def cli():
    pass


@cli.command()
def dev():
    """Run the development server"""
    # check if npm is installed
    if not setup_frontend_dev():
        return
    run_frontend_dev()
    uvicorn.run("yatta.server.app:app", port=8000, reload=True)

# def cli():
#     print("Hello from yatta.cli")
    # uvicorn.run("yatta.server.app:app", port=8000, reload=True)