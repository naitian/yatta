import { get } from "svelte/store";
import { authToken } from "./stores";
import { navigate } from "svelte-routing";
import { initialToken } from "./stores";


export const request = async (url, request, needsAuth = false) => {
    if (needsAuth && !authToken) {
        return null;
    }

    const { access_token, token_type } = get(authToken);
    const headers = {
        ...request.headers,
        "Authorization": `${token_type} ${access_token}`
    };
    const response = await fetch(url, { ...request, headers });

    if (response.ok) {
        return await response.json();
    } else if (response.status === 401 || response.status === 400) {
        authToken.set(initialToken);
        return navigate("/login");
    } else {
        const error = await response.json();
        console.error(error);
    }
}

export const login = async (username, password) => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch("/api/token", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if (!response.ok) {
        return { data, success: false };
    }

    const { access_token, token_type } = data;
    authToken.set({ access_token, token_type });
    return { data, success: true };
}

export const register = async (first_name, last_name, username, password) => {

    const response = await fetch("/api/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            first_name,
            last_name,
            username,
            password
        })
    });

    const data = await response.json();

    if (!response.ok) {
        return { data, success: false };
    }

    return { data, success: true };
}

export const logout = () => {
    authToken.set(initialToken);
}