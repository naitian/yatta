import { Outlet } from 'react-router-dom';
import { Base, Protected } from '../components/layout';
import { AuthProvider, useAuth } from '../hooks/useAuth';
import { useEffect } from 'react';

export default function Root() {
    const { user, update } = useAuth();
    useEffect(() => {
        update();
        return () => { }
    }, [])
    return (
        <Base title="Home">
            <h1>Welcome, {user.first_name}!</h1>
            <p>You've currently completed {user.num_completed} out of {user.num_assigned} annotations.</p>
        </Base>
    )
}