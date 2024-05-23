<script>
	import { request } from '../api';
	import { user, authToken } from '../stores';

	const loadUser = async () => {
		const userData = await request('/api/user', { method: 'GET' }, true);
		user.set(userData);
	};
    $: $authToken, loadUser();
</script>

{#if $user}
	<slot></slot>
{/if}
