"""Utilities for the development server."""
from yatta.utils import BASE_DIR


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
    import subprocess

    print("Running frontend development server...")
    process = subprocess.Popen(["npm", "run", "dev"], cwd=BASE_DIR)
    return process