"""Utilities for the development server."""
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
    process = subprocess.Popen(["npm", "run", "dev"], cwd=BASE_DIR)
    time.sleep(1)
    return process