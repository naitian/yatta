<script>
	import { request } from '../api';
	import { user } from '../stores';

	const loadUser = async () => {
		const userData = await request('/api/user', { method: 'GET' }, true);
		user.set(userData);
	};
	$: loadUser();
</script>

{#if $user}
	<slot></slot>
{/if}
