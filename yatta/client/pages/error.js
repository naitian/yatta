import { useRouteError } from 'react-router-dom';
export default function Error() {
    const error = useRouteError();
    return (
        <>
            <h1>Uh oh!</h1>
            <p>Sorry, an error has occurred!</p>
            <p>{error.statusText || error.message}</p>
        </>
    )
};