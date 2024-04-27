import * as React from "react";
import { HelmetProvider } from 'react-helmet-async';
import { Toaster } from 'react-hot-toast';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import { AuthProvider } from "./hooks/useAuth";
import Error from "./pages/error";
import { Protected } from "./components/layout";
import { LoginPage, RegisterPage, LogoutPage } from "./pages/login";
import Root from "./pages/root";
import Annotate from "./pages/annotate";


const router = createBrowserRouter([
    {
        path: "/",
        element: <Protected><Root /></Protected>,
        errorElement: <Error />,
    },
    {
        path: "login/",
        element: <LoginPage />,
    },
    {
        path: "register/",
        element: <RegisterPage />,
    },
    {
        path: "logout/",
        element: <LogoutPage />,
    },
    {
        path: "annotate/",
        element: <Protected><Annotate /></Protected>,
    }
])

export function App() {
    return (
        <React.StrictMode>
            <HelmetProvider>
                <AuthProvider>
                    <RouterProvider router={router} />
                    <Toaster position="bottom-right" />
                </AuthProvider>
            </HelmetProvider>
        </React.StrictMode>
    )
}
