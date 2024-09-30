export default {
    render: function ({ model, el }) {
        const text = document.createElement("p");
        el.classList.add("text-display-el");
        text.innerText = model.get("datum");
        el.appendChild(text);
    }
}