<script>
	import Protected from '../components/Protected.svelte';
	import Task from '../components/task.svelte';
	export let datum;
	export let postAssignment;
	export let next;
	export let prev;

	export let assignment;
	export let components;
	export let task;

	$: componentData = assignment.components;
	$: annotation = compileComponentAnnotations(componentData);
	let dirty = false;

	let lastSaved;

	const compileComponentAnnotations = (componentData) => {
		if (!componentData) return {};
		return Object.fromEntries(
			Object.entries(componentData).map(([componentName, { annotation }]) => {
				return [componentName, JSON.stringify(annotation)];
			})
		);
	};

	// TODO: refactor the keyboard shortcuts
	const handleKeys = (e) => {
		if (e.key === 'Enter' && !e.ctrlKey && !e.metaKey) {
			e.preventDefault();
			if (assignment.is_complete) return handleNext();
			handleComplete();
		}
		if (e.key === 'ArrowRight' && !e.ctrlKey && !e.metaKey) {
			e.preventDefault();
			handleNext();
		}
		if (e.key === 'ArrowDown' && !e.ctrlKey && !e.metaKey) {
			e.preventDefault();
			handleSkip();
		}
		if (e.key === 'ArrowLeft' && !e.ctrlKey && !e.metaKey) {
			e.preventDefault();
			handlePrev();
		}
	};

	const post = async (annotation, is_complete = false, is_skipped = false) => {
		if (!annotation) return;
		console.log('POST', annotation, is_complete, is_skipped);
		const response = await postAssignment(
			annotation,
			datum,
			is_complete || (!dirty && assignment.is_complete),
			is_skipped
		);
		assignment = response;
		annotation = assignment.annotation;
		lastSaved = new Date().toLocaleString();
	};

	const handleComplete = async () => {
		await post(annotation, true, false);
		dirty = false;
	};
	const handleSubmit = async () => {
		await handleComplete();
		await handleNext();
	};
	const handleNext = async () => {
		await post(annotation, assignment.is_complete, assignment.is_skipped);
		return next(assignment);
	};
	const handleSkip = async () => {
		// when skipping, mark as incomplete even if it was marked as complete
		dirty = true;
		await post(annotation, false, true);
	};
	const handlePrev = async () => {
		await post(annotation, assignment.is_complete, assignment.is_skipped);
		return prev(assignment);
	};

	// This constantly saves the annotation, which prevents lost work
	// BUT complicates the logic for is_complete
	// We just save when the user presses one of the buttons instead for now
	// $: postAssignment(annotation);
</script>

<svelte:window on:keydown={handleKeys} />

<main class="p-5">
	{#if assignment.is_complete}
		<div class="bg-green-300 p-3">
			<h1>Marked as complete.</h1>
		</div>
	{:else if assignment.is_skipped}
		<div class="bg-red-300 p-3">
			<h1>Marked as skipped.</h1>
		</div>
	{:else}
		<div class="bg-gray-100 p-3 text-gray-400">
			<h1>Not yet marked as complete. Press submit to mark as complete.</h1>
		</div>
	{/if}
	<Task {task} {components} bind:componentData bind:dirty />
	<div class="info text-sm text-gray-300 flex my-8">
		<span>{lastSaved ? `Last saved ${lastSaved}.` : ''}</span>
		<div class="flex-1"></div>
		<span class="flex-none"><a href="/annotate/{datum}">@{datum}</a></span>
	</div>
	<div class="actions mx-auto max-w-fit">
		<button class="btn btn-lg mx-4" on:click={handlePrev} disabled={assignment.prev === null}
			>Prev</button
		>
		<button class="btn btn-lg mx-4 btn-success" on:click={handleSubmit}>Submit</button>
		<button class="btn btn-lg mx-4 btn-error" on:click={handleSkip}>Skip</button>
	</div>
</main>

<!-- <button>Bookmark</button> -->

<style>
	.actions {
		display: flex;
		justify-content: space-between;
	}
</style>
