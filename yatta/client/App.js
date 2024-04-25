import * as React from "react";
import { HelmetProvider } from 'react-helmet-async';
import { Toaster } from 'react-hot-toast';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import { AuthProvider } from "./hooks/useAuth";
import Error from "./pages/error";
import { LoginPage, RegisterPage, LogoutPage } from "./pages/login";
import Root from "./pages/root";


const router = createBrowserRouter([
    {
        path: "/",
        element: <Root />,
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
