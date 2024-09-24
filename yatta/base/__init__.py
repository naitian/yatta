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
        self.props["placeholder"] = placeholder


class TextDisplay(Component):
    """A simple text display component"""

    name = "text-display"
    _esm = relative_path("./text-display/index.js")


class Checkboxes(Component):
    """A multiple choice checkbox component"""

    name = "checkboxes"

    _esm = """
    export default {
        render: function ({ model, el }) {
            const { choices } = model.get("props");
            let annotation = model.get("annotation") || [];
            choices.forEach(function (choice) {
                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.value = choice;
                checkbox.checked = annotation.includes(choice);
                checkbox.addEventListener("change", function () {
                    if (checkbox.checked && !annotation.includes(choice)) {
                        annotation.push(choice);
                    } else {
                        annotation = annotation.filter(function (item) {
                            return item !== choice;
                        });
                    }
                    model.set("annotation", choice);
                });
                el.appendChild(checkbox);
                el.appendChild(document.createTextNode(choice));
                el.appendChild(document.createElement("br"));
            });
        }
    }
    """
    _css = """
    input[type="checkbox"] {
        margin-right: 10px;
    }
    """

    def __init__(self, choices: list[str], **kwargs):
        super().__init__(**kwargs)
        self.props["choices"] = choices
