import { getAnnotationAssignment, getTask } from '$lib/api.js';
export async function load({ params }) {
    const task = await getTask();
    const assignment = await getAnnotationAssignment(+params.datum_id);

    console.log(assignment)
    return {
        task,
        assignment,
        datum_id: +params.datum_id,
    }
}