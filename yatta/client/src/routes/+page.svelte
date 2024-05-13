<script>
	import { user } from '$lib/stores';
	import { refreshToken } from '$lib/api';
	import Page from '$lib/components/Page.svelte';
	import Button from '$lib/components/ui/button/button.svelte';

	let title = 'Dashboard';

	refreshToken();
</script>

<Page {title} needsAuth={true}>
	<p class="leading-7 [&:not(:first-child)]:mt-6">
		Hi, {$user.username}! You have completed {$user.num_completed}/{$user.num_assigned} annotations.
	</p>

	{#if $user.next_assignment === null}
		<p class="mt-6 leading-7">You have no more assignments. Check back later!</p>
	{:else}
		<p class="mt-6 leading-7">
			You have {$user.num_assigned - $user.num_completed} assignments remaining.
		</p>
		<Button href="/annotate/{$user.next_assignment}">Start annotating!</Button>
	{/if}
</Page>
