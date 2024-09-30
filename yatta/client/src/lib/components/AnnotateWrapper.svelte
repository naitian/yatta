<script>
	import { navigate } from 'svelte-routing';
	import { request } from '../api';
	import Annotate from '../pages/annotate.svelte';
	import Protected from './Protected.svelte';
	export let datum;
	let hmr = false;

	let socket;
	// TODO: extract HMR logic to a separate file
	(() => {
		socket = new WebSocket(`ws://${window.location.host}/hmr`);
		const tryReload = () => {
			// TODO: in the future, we might want to reload also on server restart
			// (i.e., on close event)
			console.log('[HMR] Reloading...');
			hmr = !hmr;
		};
		const tryReconnect = () => {
			const maxAttempts = 10;
			const interval = 100;

			let attempts = 0;
			const reconnect = () => {
				if (socket.readyState === WebSocket.OPEN) {
					return;
				}
				if (attempts >= maxAttempts) {
					console.error('[HMR] Could not reconnect to server');
					return;
				}
				attempts++;
				setTimeout(() => {
					console.log(`[HMR] Attempting to reconnect... (${attempts})`);
					socket = new WebSocket(`ws://${window.location.host}/hmr`);
					socket.addEventListener('open', () => {
						console.log('[HMR] Reconnected');
						tryReload();
					});
					socket.addEventListener('close', reconnect);
				}, interval);
			};
			reconnect();
		};
		socket.addEventListener('open', () => {
			console.info(`[HMR] Listening for HMR updates at ${socket.url}`);
		});
		socket.addEventListener('message', (event) => {
			if (event.data === 'reload') {
				tryReload();
			}
		});
		socket.addEventListener('close', () => {
			tryReconnect();
		});
	})();

	const loadTask = async () => {
		let { task, components } = await request(`/api/task`, { method: 'GET' }, true);
		return { task, components };
	};

	const loadAssignment = async (datum) => {
		const assignmentData = await request(`/api/annotate/${datum}`, { method: 'GET' }, true);
		return assignmentData;
	};

	const load = async (datum) => {
		// TODO: refactor this so we only run loadTask once, since it's the same
		// for all annotation assignments
		const { task, components } = await loadTask();
		const assignment = await loadAssignment(datum);
		return { task, components, assignment };
	};

	const postAssignment = async (annotation, datum, is_complete = false, is_skipped = false) => {
		if (!annotation) return;
		const response = await request(
			`/api/annotate/${datum}`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					annotation,
					is_complete,
					is_skipped
				})
			},
			true
		);
		return response;
	};

	const next = async (assignment) => {
		if (assignment.next === null) return navigate(`/`);
		return navigate(`/annotate/${assignment.next}`);
	};
	const prev = async (assignment) => {
		if (assignment.prev === null) return;
		return navigate(`/annotate/${assignment.prev}`);
	};
</script>

<Protected>
	{#key hmr}
		{#await load(datum) then { task, components, assignment }}
			<Annotate {task} {components} {assignment} {postAssignment} {next} {prev} {datum} />
		{/await}
	{/key}
</Protected>
