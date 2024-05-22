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

	const destroyFunctions = [];

	const renderTask = () => {
		container.innerHTML = '';
		Object.entries(task).forEach(([field, component]) => {
			const { module, cssPath } = components[component.name];
			const { render } = module;
			const componentContainer = document.createElement('div');

			const style = document.createElement('link');
            style.rel = 'stylesheet';
            style.href = cssPath;
			container.appendChild(style);

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
				if (annotation[field] === data['annotation']) return;
				annotation[field] = data['annotation'];
				dirty = true;
			});
			const destroy = render({
				el: componentContainer,
				model
			});
			destroyFunctions.push(destroy);
		});
	};

	onMount(() => {
		renderTask();
		return () => {
			destroyFunctions.forEach((destroy) => destroy());
		};
	});
</script>

<div class="container min-h-96 p-5" bind:this={container}></div>
