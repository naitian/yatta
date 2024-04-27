"""Settings manager for server.

This is _not_ the default config file. This contains utilities to load and
provide settings.
"""

import importlib
import importlib.util
from functools import lru_cache
from typing import Any

from yatta.utils import INTERNAL_CONFIG_PATH


class Settings:
    """Settings manager for the server."""

    _settings = None

    def __init__(self):
        self._settings = self.load()

    @lru_cache
    def load(self):
        """Load settings from the given module."""
        spec = importlib.util.spec_from_file_location(
            INTERNAL_CONFIG_PATH.stem, INTERNAL_CONFIG_PATH
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def __getattr__(self, name: str) -> Any:
        return getattr(self._settings, name.upper())

settings = Settings()
