<script>
	import { onMount } from 'svelte';
	import { logout } from '../api';
	import { navigate } from 'svelte-routing';

    const handleLogout = async () => {
        logout();
        navigate('/login', {replace: true});
    };
    onMount(() => {
        handleLogout();
    });
</script>