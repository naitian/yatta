<script>
	import Page from '$lib/components/Page.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import Input from '$lib/components/ui/input/input.svelte';
	import Label from '$lib/components/ui/label/label.svelte';

	import { goto } from '$app/navigation';
	import { login } from '$lib/api';
	import { user } from '$lib/stores';

	let username = '';
	let password = '';

	if ($user) {
		goto('/');
	}

	const submit = async () => {
		try {
			await login(username, password);
			console.log("Done!")
			goto('/');
		} catch (error) {
			console.error(error);
		}
	};
</script>

<Page title="Login">
	<form>
		<div>
			<Label for="username">Username</Label>
			<Input type="text" bind:value={username} />
		</div>
		<div>
			<Label for="password">Password</Label>
			<Input type="password" bind:value={password} />
		</div>
		<div>
			<Button type="submit" on:click={submit}>Login</Button>
			<a href="/register"><Button variant="link">Register</Button></a>
		</div>
	</form>
</Page>

<style>
	form {
		@apply flex max-w-md flex-col space-y-4;
	}
</style>
