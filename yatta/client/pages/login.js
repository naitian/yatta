// Login page
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { Base } from "../components/layout"
import { Link } from "react-router-dom";
import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const sendCredentials = async (username, password, path) => {
    const response = await fetch(path, {
        method: "POST",
        body: formData,
    });
    return response.json();
}

export function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { user, login } = useAuth();
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch("/api/token", {
            method: "POST",
            body: formData,
        })
        const json = await response.json();
        if (!response.ok) {
            toast.error(`Login failed: ${json.detail || response.statusText}`);
            return;
        }

        console.log("JSON")
        login(json)
    }

    return (
        <Base title="Login">
            { user && <Navigate to="/" replace={true} />}
            <h1>Login</h1>
            <form>
                <label>
                    Username
                    <input
                        type="text" name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </label>
                <label>
                    Password
                    <input
                        type="password" name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </label>
                <button onClick={handleSubmit}>Login</button>
            </form>
            <Link to="/register">Register an account</Link>
        </Base>
    )
}

export function RegisterPage() {
    const [firstname, setFirstname] = useState("");
    const [lastname, setLastname] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();

        response = await fetch("/api/register", {
            method: "POST",
            body: JSON.stringify({ first_name: firstname, last_name: lastname, username, password }),
            headers: {
                "Content-Type": "application/json",
            },
        });
        json = await response.json();
        if (!response.ok) {
            setError(`Registration failed: ${json.detail || response.statusText}`);
            setSuccess(false);
            return
        } else {
            setError(null);
            setSuccess(true);
        }
    }

    // I feel like this is a bit much...
    useEffect(() => {
        if (error) toast.error(error);
    }, [error])

    useEffect(() => {
        if (success) toast.success("Registration successful!");
    }, [success])

    return (
        <Base title="Register">
            {success && <Navigate to="/login" replace={true} />}
            <h1>Register</h1>
            <form>
                <label>
                    First Name
                    <input
                        type="text" name="first_name"
                        value={firstname}
                        onChange={(e) => setFirstname(e.target.value)}
                    />
                </label>
                <label>
                    Last Name
                    <input
                        type="text" name="last_name"
                        value={lastname}
                        onChange={(e) => setLastname(e.target.value)}
                    />
                </label>
                <label>
                    Username
                    <input
                        type="text" name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </label>
                <label>
                    Password
                    <input
                        type="password" name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </label>
                <button onClick={handleSubmit}>Register</button>
            </form>
            <Link to="/login">Log in instead</Link>
        </Base>
    )
}


export function LogoutPage() {
    const { user, logout } = useAuth();
    useEffect(() => {
        logout();
    }, [])
    return (<Base title="Logout">
        {user ? `Logging out...` : `You've been logged out!`}</Base>)
}