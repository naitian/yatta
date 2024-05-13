"""Settings manager for server.

This is _not_ the default config file. This contains utilities to load and
provide settings.
"""

import importlib
import importlib.util
from functools import lru_cache

from yatta.utils import INTERNAL_CONFIG_PATH


@lru_cache
def load_settings(settings_name: str = "default"):
    """Load settings from the given module."""
    spec = importlib.util.spec_from_file_location(
        INTERNAL_CONFIG_PATH.stem, INTERNAL_CONFIG_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, settings_name):
        return getattr(module, settings_name)
    else:
        raise ValueError(
            f"Settings {settings_name} not found in {INTERNAL_CONFIG_PATH.resolve()}"
        )


settings = load_settings()
