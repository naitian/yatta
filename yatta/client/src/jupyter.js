import "./app.css"
import Annotate from "./lib/pages/annotate.svelte"


// This also feels pretty janky -- probably worth thinking about whether this
// approach is the best way to handle this.
// Especially bc custom events are the dispreferred way to communicate between
// JS and Python:
// https://anywidget.dev/en/jupyter-widgets-the-good-parts/#2-custom-messages:~:text=Prefer%20Traitlets%20over%20custom%20messages%20for%20state%20synchronization
function eventToPromise(model, object_name) {
    return new Promise((resolve, reject) => {
        const listener = ({ name, data }) => {
            resolve(model.get(object_name));
            model.off(name, listener)
        }

        model.on(`on:${object_name}`, listener)
        setTimeout(() => reject(new Error("Timeout")), 2000)
    })
}



export default ({
    render: ({ model, el }) => {
        const datum = model.get('datum')
        const { task, components } = model.get('task')
        const assignment = model.get('assignment')

        model.on("change:datum", () => {
            component.$set({ datum: model.get('datum') })
        })
        model.on("change:assignment", () => {
            component.$set({ assignment: model.get('assignment') })
        })
        model.on("change:task", () => {
            const { task, components } = model.get('task')
            component.$set({ task, components })
        })

        const postAssignment = async (annotation, datum, is_complete = false, is_skipped = false) => {
            model.set("result", {
                annotation, is_complete, is_skipped
            })
            model.save_changes();
            return eventToPromise(model, "change:assignment")
        }

        const next = async () => {
            model.set("datum", datum + 1)
        }

        const prev = async () => {
            model.send({ event: 'prev' })
        }

        let component = new Annotate({
            target: el, props: {
                datum,
                task,
                components,
                assignment,
                postAssignment,
                prev,
                next,
            }
        })
        return () => {
            component.$destroy()
        }
    }
})