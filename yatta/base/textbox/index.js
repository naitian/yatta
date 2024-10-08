export default {
    render: function ({ model, el }) {
        const textbox = document.createElement("input");
        const { placeholder } = model.get("props");
        textbox.type = "text";
        console.log(model.get("annotation"));
        textbox.value = model.get("annotation") || "";
        textbox.placeholder = placeholder;

        textbox.addEventListener("input", function () {
            model.set("annotation", textbox.value);
        });
        textbox.classList.add("textbox-el");
        el.appendChild(textbox);
    }
}