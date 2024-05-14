<script>
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { Model } from '../model';

	export let task;
	export let components;
	export let datum;
	export let annotation;
    export let dirty;

	let container;

	const renderTask = () => {
		container.innerHTML = '';
		Object.entries(task).forEach(([field, component]) => {
			const { render } = components[component.name];
			const componentContainer = document.createElement('div');
			container.appendChild(componentContainer);

			const props = component.props || {};
			const fieldAnnotation = annotation?.[field] || {};
			const model = Model({
				datum,
				annotation: fieldAnnotation,
				props
			});
			model.on('change', ({ detail }) => {
				const { data } = detail;
				if (!annotation) annotation = {};
                if (annotation[field] === data['annotation'])
                    return;
				annotation[field] = data['annotation'];
                dirty = true;
			});
			render({
				el: componentContainer,
				model
			});
		});
	};

	onMount(() => {
		renderTask();
	});
</script>

<div class="container min-h-96 p-5" bind:this={container}></div>
