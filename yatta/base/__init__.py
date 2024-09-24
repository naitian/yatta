"""
A basic set of components.
"""

from yatta.core.plugins import Component
from yatta.utils import relative_path


print(relative_path("./textbox/index.js"))


class Textbox(Component):
    """A simple textbox component"""

    name = "textbox"
    _esm = relative_path("./textbox/index.js")
    _css = relative_path("./textbox/index.css")

    def __init__(self, placeholder=None, **kwargs):
        super().__init__(**kwargs)
        self.placeholder = placeholder

    def transform(self, datum):
        datum = super().transform(datum)
        return {"datum": datum, "placeholder": self.placeholder or ""}
