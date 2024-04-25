"""Utilities for the development server."""

from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from yatta.utils import BASE_DIR, SRC_DIR


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
    subprocess.run(["npm", "install"], cwd=BASE_DIR)
    return True


def run_frontend_dev():
    """Run the frontend development server."""
    import shutil
    import subprocess
    import time

    print("Running frontend development server...")
    shutil.rmtree(SRC_DIR / "client" / "dist", ignore_errors=True)
    shutil.rmtree(BASE_DIR / ".parcel-cache", ignore_errors=True)
    process = subprocess.Popen(["npm", "run", "dev"], cwd=BASE_DIR)
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
