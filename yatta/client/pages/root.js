import { useEffect } from 'react';
import { Base } from '../components/layout';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

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
            <Link to="/annotate">Start annotating</Link>
        </Base>
    )
}