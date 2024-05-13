"""Plugin manager"""

from dataclasses import dataclass
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel

from yatta.server.dev import setup_frontend_dev


def get_plugins():
    """Get all plugins."""
    return {
        str(name): module.load()
        for name, module in dict(entry_points(group="yatta.plugins")).items()
    }


def setup_plugins():
    """Setup all plugins."""
    plugins = get_plugins()
    if len(plugins) == 0:
        return


@dataclass(kw_only=True)
class Component:
    """Base class for components"""

    name: str
    _esm: str | Path
    _css: str | Path = ""
    props: dict | None = None
    transform: Callable[[Any], dict] = lambda x: str(x)

    def __post_init__(self):
        if self.name is None:
            self.name = self.__class__.__name__

        self._esm = self._read_file_if_path(self._esm)
        self._css = self._read_file_if_path(self._css)

    def _read_file_if_path(self, path):
        if isinstance(path, Path):
            with open(path, "r") as f:
                return f.read()
        return path

    def to_dict(self):
        """
        Convert to a dictionary but exclude the transform function, _esm, and _css.
        """
        return {
            k: v
            for k, v in self.__dict__.items()
            if k not in ["transform", "_esm", "_css"]
        }
