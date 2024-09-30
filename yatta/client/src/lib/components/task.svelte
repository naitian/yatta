<script>
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { Model } from '../model';

	export let task;
	export let components;
	export let componentData;
	export let dirty;

	let container;

	// For now, I'm just taking these from anywidget (this whole multi-step
	// translation to/from anywidget could probably be more elegant)
	/**
	 * @param {string} str
	 * @returns {str is "https://${string}" | "http://${string}"}
	 */
	function is_href(str) {
		return str.startsWith('http://') || str.startsWith('https://');
	}

	/**
	 * @param {string} href
	 * @param {string} anywidget_id
	 * @returns {Promise<void>}
	 */
	async function load_css_href(href, anywidget_id) {
		/** @type {HTMLLinkElement | null} */
		let prev = document.querySelector(`link[id='${anywidget_id}']`);

		// Adapted from https://github.com/vitejs/vite/blob/d59e1acc2efc0307488364e9f2fad528ec57f204/packages/vite/src/client/client.ts#L185-L201
		// Swaps out old styles with new, but avoids flash of unstyled content.
		// No need to await the load since we already have styles applied.
		if (prev) {
			let newLink = /** @type {HTMLLinkElement} */ (prev.cloneNode());
			newLink.href = href;
			newLink.addEventListener('load', () => prev?.remove());
			newLink.addEventListener('error', () => prev?.remove());
			prev.after(newLink);
			return;
		}

		return new Promise((resolve) => {
			let link = Object.assign(document.createElement('link'), {
				rel: 'stylesheet',
				href,
				onload: resolve
			});
			document.head.appendChild(link);
		});
	}

	/**
	 * @param {string} css_text
	 * @param {string} anywidget_id
	 * @returns {void}
	 */
	function load_css_text(css_text, anywidget_id) {
		/** @type {HTMLStyleElement | null} */
		let prev = document.querySelector(`style[id='${anywidget_id}']`);
		if (prev) {
			// replace instead of creating a new DOM node
			prev.textContent = css_text;
			return;
		}
		let style = Object.assign(document.createElement('style'), {
			id: anywidget_id,
			type: 'text/css'
		});
		style.appendChild(document.createTextNode(css_text));
		document.head.appendChild(style);
	}

	/**
	 * @param {string | undefined} css
	 * @param {string} anywidget_id
	 * @returns {Promise<void>}
	 */
	async function load_css(css, anywidget_id) {
		if (!css || !anywidget_id) return;
		if (is_href(css)) return load_css_href(css, anywidget_id);
		return load_css_text(css, anywidget_id);
	}

	/**
	 * @param {string} esm
	 * @returns {Promise<{ module: any, url: string }>}
	 */
	async function load_esm(esm) {
		if (is_href(esm)) {
			return {
				module: await import(/* webpackIgnore: true */ esm),
				url: esm
			};
		}
		let url = URL.createObjectURL(new Blob([esm], { type: 'text/javascript' }));
		let module = await import(/* webpackIgnore: true */ url);
		URL.revokeObjectURL(url);
		return { module: module.default, url };
	}

	const destroyFunctions = [];

	const load_all_esm = async (components) => {
		return Object.fromEntries(
			await Promise.all(
				Object.values(components).map(async ({ name, esm }) => {
					const output = await load_esm(esm);
					return [name, output];
				})
			)
		);
	};

	const load_components = async (components) => {
		Object.entries(components).forEach(([name, { css }]) => {
			load_css(css, name);
		});
		return load_all_esm(components);
	};

	const renderTask = async () => {
		container.innerHTML = '';
		const esm_modules = await load_components(components);
		task.forEach(({field, component}) => {
			let { name, props } = component;
			const { module } = esm_modules[name];
			const { render } = module;

			const componentContainer = document.createElement('div');
			container.appendChild(componentContainer);
			props = props || {};
			const fieldAnnotation = componentData[field].annotation;
			const fieldDatum = componentData[field].datum;

			const model = Model({
				datum: fieldDatum,
				annotation: fieldAnnotation,
				props
			});
			model.on('change', ({ detail }) => {
				const { data } = detail;
				if (componentData[field].annotation === data['annotation']) return;
				componentData[field].annotation = data['annotation'];
				dirty = true;
			});
			const destroy = render({
				el: componentContainer,
				model
			});
			if (destroy) destroyFunctions.push(destroy);
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
