// Page layout templates
import { Helmet } from "react-helmet-async";
import { useAuth } from "../hooks/useAuth";
import { Navigate } from "react-router-dom";

export function Base({ title, children }) {
    return (
        <>
            <Helmet>
                <title>{title}</title>
            </Helmet>
            <div className="content">
                {children}
            </div>
        </>
    )
}

export function Protected({ children }) {
    const { user } = useAuth();
    if (!user) {
        return <Navigate to="/login" replace={true}/>
    }
    return children
}