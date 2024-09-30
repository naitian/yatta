import { navigate } from "svelte-routing";


export const request = async (url, request, needsAuth = false) => {
    const headers = {
        ...request.headers,
    };
    const response = await fetch(url, { ...request, headers });

    if (response.ok) {
        return await response.json();
    } else if (response.status === 401 || response.status === 400) {
        return navigate("/login");
    } else {
        const error = await response.json();
        console.error(error);
    }
}

export const login = async (username, password) => {
    const response = await fetch("/api/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
        headers: {
            "Content-Type": "application/json"
        }
    });

    const data = await response.json();

    if (!response.ok) {
        return { data, success: false };
    }
    return navigate("/");
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
    request("/api/logout", { method: "GET" });
}