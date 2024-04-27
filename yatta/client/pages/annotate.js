import { useEffect, useState, useMemo } from "react";
import { Base } from "../components/layout"
import { useAuth } from "../hooks/useAuth";


const loadTask = async ({ task, dependencies }) => {
    // deps = await Promise.all(dependencies.map(async (dep) => import(`/plugins/${dep}`)))
    // components = Object.assign({}, ...deps.map((dep) => dep.components))
    // console.log(components)
}


function TaskManager() {

    const [task, setTask] = useState(null);
    const { user } = useAuth();

    useEffect(() => {
        const fetchTask = async () => {
            const response = await fetch("/api/task", {
                headers: {
                    "Authorization": `Bearer ${user.access_token}`,
                },
            });
            const json = await response.json();
            console.log(json)
            setTask(json);
        }
        fetchTask();
        return () => { setTask(null) }
    }, [])

    const taskComponent = useMemo(() => {
        if (!task) return null;
        return loadTask(task);
    }, [task])

    return (
        <div>This is an annotation task.</div>
    )

}

export default function Annotate() {
    return (
        <Base>
            <h1>Annotate</h1>
            <p>Here is where you will annotate.</p>
            <TaskManager />
        </Base>
    )
}