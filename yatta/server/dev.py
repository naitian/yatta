"""Utilities for the development server."""

import os
from typing import Coroutine
from baize.asgi import Files
from baize.typing import Receive, Scope, Send
from fastapi.exceptions import HTTPException
from fastapi.responses import Response as FastApiResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from yatta.utils import FRONTEND_DIR, SRC_DIR

SERVER_DEV_PORT = 4123


def setup_frontend_dev():
    """Set up the frontend for development."""
    import shutil
    import subprocess

    # check if npm is installed
    if not shutil.which("npm"):
        print("npm is required to run the development server")
        return False

    # install frontend dependencies
    print("Installing frontend dependencies...")
    subprocess.run(["npm", "install"], cwd=FRONTEND_DIR)
    return True


def run_frontend_dev(port=5173):
    """Run the frontend development server."""
    import shutil
    import subprocess
    import time

    print("Running frontend development server...")
    shutil.rmtree(SRC_DIR / "client" / "dist", ignore_errors=True)
    process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", str(port)], cwd=FRONTEND_DIR
    )
    # We sleep to (I think) avoid a race condition where starlette tries to
    # access the dist/ folder before everything is built.
    # TODO: handle this maybe by waiting for the first build to finish
    time.sleep(1)
    return process


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex


class BaizeStaticFiles(Files):
    def __call__(self, scope, receive, send):
        scope["path"] = os.path.relpath(scope["path"], scope["root_path"])
        return super().__call__(scope, receive, send)
