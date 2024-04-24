"""Utility functions for use by the server and users."""

import inspect
from pathlib import Path


def relative_path(path):
    """Return an absolute path relative to the current file."""
    # use inspect.stack()[1] to get the caller's filename
    module_path = inspect.stack()[1].filename
    return Path(module_path).parent / path


# directory for source code
SRC_DIR = relative_path(".")
BASE_DIR = SRC_DIR / ".."

# internal path to the config file
INTERNAL_CONFIG_PATH = SRC_DIR / "config" / "__internal.py"

def link_config_path(config_path: Path | str) -> None:
    """Create symlink from the internal config to the given path."""
    import os
    if INTERNAL_CONFIG_PATH.exists():
        INTERNAL_CONFIG_PATH.unlink()
    os.symlink(Path(config_path).resolve(), INTERNAL_CONFIG_PATH)