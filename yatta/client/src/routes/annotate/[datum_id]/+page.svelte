<script>
    import Page from '$lib/components/Page.svelte';
    import MovieTask from '$lib/components/MovieTask.svelte';
    import { postAnnotation } from '$lib/api.js';
    export let data;

    const {task, assignment, datum_id} = data;
    let {datum, annotation} = assignment;

    $: postAnnotation(datum_id, {"utterances": annotation});
</script>


<Page needsAuth={true}>
    <MovieTask {datum} bind:annotation />
</Page>