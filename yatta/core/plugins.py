"""Plugin manager"""

from pathlib import Path
from typing import Any, Callable


class Component:
    """Base class for components

    TODO: Add a transform function to transform the data before sending it to
    the frontend. This requires modifications to how the API serves the data.
    """

    name: str
    _esm: str | Path
    _css: str | Path = ""

    def __init__(
        self,
        dev: bool = False,
        transform_fn: Callable[[Any], Any] | None = None,
        props: dict[str, Any] = {},
    ):
        self.dev = dev
        self.transform_fn = transform_fn
        self.props = props

        if self.name is None:
            self.name = self.__class__.__name__

        if not self.dev:
            self._esm = self._read_file_if_path(self._esm)
            self._css = self._read_file_if_path(self._css)

    def _read_file_if_path(self, path):
        if isinstance(path, Path):
            with open(path, "r") as f:
                return f.read()
        return path

    def transform(self, datum: Any) -> Any:
        if self.transform_fn is not None:
            return self.transform_fn(datum)
        return datum

    @property
    def esm(self):
        if self.dev:
            return self._read_file_if_path(self._esm)
        return self._esm

    @property
    def css(self):
        if self.dev:
            return self._read_file_if_path(self._css)
        return self._css

    def to_dict(self):
        """
        Convert to a dictionary but exclude the transform function, _esm, and _css.
        """
        return {
            "name": self.name,
            "props": self.props,
        }
