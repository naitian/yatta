<script>
	import { link } from 'svelte-routing';
	import Protected from '../components/Protected.svelte';
	import { user } from '../stores';
</script>

<Protected>
	<main class="p-10">
		<h1 class="text-lg font-bold">Hey, {$user.first_name}!</h1>
		<p class="my-3">
			You have completed {$user.num_completed} / {$user.num_assigned} annotations. You have skipped {$user.num_skipped}
			/ {$user.num_assigned} annotations.
		</p>
		<p class="my-3">
			You have {$user.num_assigned - $user.num_completed - $user.num_skipped} / {$user.num_assigned}
			assignments left to view.
		</p>
		{#if $user.next_assignment !== null}
			<a href="/annotate/{$user.next_assignment}" use:link
				><button class="btn btn-primary btn-sm">Start annotating</button></a
			>
		{/if}
	</main>
</Protected>
