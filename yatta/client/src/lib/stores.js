import { writable } from "svelte/store";


export let initialToken = { access_token: null, token_type: null};
try {
    initialToken = JSON.parse(localStorage.getItem("authToken")) || initialToken;
} catch (e) {
    console.error(e);
}
export const authToken = writable(initialToken);
authToken.subscribe((value) => {
    if (value) {
        localStorage.setItem("authToken", JSON.stringify(value));
    }
});


export const user = writable(null);

export const task = writable(null);