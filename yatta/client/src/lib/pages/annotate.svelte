<script>
	import { navigate } from 'svelte-routing';
	import { request } from '../api';
	import Task from '../components/task.svelte';
	import Protected from '../components/Protected.svelte';
	export let datum;

	let assignment;
	let components;
	let task;
	let annotation;
	let dirty = false;

	let lastSaved;

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

	const loadTask = async () => {
		const taskData = await request(`/api/task`, { method: 'GET' }, true);
		components = Object.fromEntries(
			await Promise.all(
				taskData.components.map(async (name) => {
					const module = await import(`/api/component/${name}`);
					const cssPath = `/api/css/${name}`;
					return [name, { module: module.default, cssPath }];
				})
			)
		);
		task = taskData.task;
	};

	const loadAssignment = async (datum) => {
		const assignmentData = await request(`/api/annotate/${datum}`, { method: 'GET' }, true);
		assignment = assignmentData;
		annotation = assignment.annotation;
	};

	const postAssignment = async (annotation, is_complete = false, is_skipped = false) => {
		if (!annotation) return;
		const response = await request(
			`/api/annotate/${datum}`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					annotation: JSON.stringify(annotation),
					is_complete: is_complete || (!dirty && assignment.is_complete),
					is_skipped: is_skipped
				})
			},
			true
		);
		assignment = response;
		annotation = assignment.annotation;
		lastSaved = new Date().toLocaleString();
	};

	const handleComplete = async () => {
		await postAssignment(annotation, true, false);
		dirty = false;
	};
	const handleSubmit = async () => {
		await handleComplete();
		await handleNext();
	};
	const handleNext = async () => {
		if (assignment.next === null) return navigate(`/`);
		return navigate(`/annotate/${assignment.next}`);
	};
	const handleSkip = async () => {
		// when skipping, mark as incomplete even if it was marked as complete
		dirty = true;
		await postAssignment(annotation, false, true);
	};
	const handlePrev = async () => {
		if (assignment.prev === null) return;
		await postAssignment(annotation, assignment.is_complete, assignment.is_skipped);
		return navigate(`/annotate/${assignment.prev}`);
	};

	// This constantly saves the annotation, which prevents lost work
	// BUT complicates the logic for is_complete
	// We just save when the user presses one of the buttons instead for now
	// $: postAssignment(annotation);
</script>

<svelte:window on:keydown={handleKeys} />
<Protected>
	{#await Promise.all([loadAssignment(datum), loadTask()]) then}
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
			<Task {task} {components} datum={assignment.datum} bind:annotation bind:dirty />
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
	{/await}
</Protected>

<style>
	.actions {
		display: flex;
		justify-content: space-between;
	}
</style>
