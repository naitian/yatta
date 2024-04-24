"""Utility functions for use by the server and users."""

import inspect
from pathlib import Path


def relative_path(path):
    """Return an absolute path relative to the current file."""
    # use inspect.stack()[1] to get the caller's filename
    module_path = inspect.stack()[1].filename
    return Path(module_path).parent / path