import { Outlet } from 'react-router-dom';
import { Protected } from '../components/layout';
import { AuthProvider } from '../hooks/useAuth';
export default function Root() {
    return (
            <Protected>
                <header>This is a header, potentially a nav bar</header>
                <div>
                    <Outlet />
                </div>
            </Protected>

    )
}