export default {
    render: function ({ model, el }) {
        const text = document.createElement("p");
        text.innerText = model.get("datum");
        text.style.lineHeight = "1.5";
        el.appendChild(text);
    }
}