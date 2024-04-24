import * as React from "react";
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Root from "./pages/root";
import Error from "./pages/error";


const router = createBrowserRouter([
    {
        path: "/",
        element: <Root />,
        errorElement: <Error />,
    },
])

export function App() {
    return (
        <React.StrictMode>
            <RouterProvider router={router} />
        </React.StrictMode>
    )
}
