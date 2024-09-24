from dataclasses import dataclass
from pathlib import Path

from yatta.core.plugins import Component


@dataclass(kw_only=True)
class Textbox(Component):
    """A simple textbox component"""

    name: str = "textbox"
    _esm: str | Path = """
    export default {
    render: function ({ model, el }) {
        console.log(model.get("datum"))
        el.innerHTML = model.get("datum").text;
        el.className = `textrender textrender-${model.cid}`
    }
    }
    """
