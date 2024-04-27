import { createContext, useContext, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "./useLocalStorage";

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useLocalStorage("user", null);

    const login = (user) => {
        setUser(user);
    };

    const logout = () => {
        setUser(null);
    };

    const update = async () => {
        if (!user) return
        const response = await fetch("/api/refresh", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${user.access_token}`,
            },
        });
        const newUser = await response.json();
        if (!response.ok) {
            setUser(null);
            return;
        }
        setUser(newUser);
    }

    const value = useMemo(() => ({ user, login, logout, update }), [user]);

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
    return useContext(AuthContext);
}