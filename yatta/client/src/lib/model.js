/*
    Backbone-like model interface
    Implements the following:
    - Model.set(key, value) - sets the value of the key
    - Model.get(key) - gets the value of the key
    - Model.on(event, callback) - listens to the event
    
    A shorter/worse version of
    https://github.com/manzt/anywidget/blob/b4557b3ef9d8727337acba36ec5b68d6cbc37990/packages/deno/src/mod.ts#L159
*/

let idCounter = 0;
const uniqueId = (prefix) => (prefix ?? '') + ++idCounter;


const deepcopy = (data) => JSON.parse(JSON.stringify(data));
export const Model = (attributes) => ({
    _state: attributes,
    _target: new EventTarget(),
    cid: uniqueId("model"),
    set: function (key, value) {
        const previous = deepcopy(this._state[key]);
        this._state[key] = value;
        this._target.dispatchEvent(new CustomEvent("change", {
            detail: {
                data: deepcopy(this._state),
                previous,
                changed: { [key]: value }
            }
        }));
    },
    get: function (key) {
        return this._state[key];
    },
    on: function (event, callback) {
        this._target.addEventListener(event, callback);
    },
})