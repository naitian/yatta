from yatta.core.plugins import Component


class Textbox(Component):
    """A simple textbox component"""

    name = "textbox"
    _esm = """
    export default {
        render: function ({ model, el }) {
            const textbox = document.createElement("input");
            textbox.type = "text";
            console.log(model.get("annotation"));
            textbox.value = model.get("annotation") || "";

            textbox.addEventListener("input", function () {
                model.set("annotation", textbox.value);
            });
            el.appendChild(textbox);
        }
    }
    """
