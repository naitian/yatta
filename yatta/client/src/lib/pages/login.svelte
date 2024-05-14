<script>
	import { link, navigate } from 'svelte-routing';
	import { login } from '../api';

	let username = '';
	let password = '';
	let error = null;

	const submit = async () => {
		const { success } = await login(username, password);
		if (success) navigate('/');
		error = 'Something went wrong!';
	};
</script>

<main>
	<form>
		<label for="username" class="form-control w-full max-w-xs">
			<div class="label">
				<span class="label-text">Username</span>
			</div>
			<input type="text" class="input input-bordered w-full max-w-xs" bind:value={username} />
		</label>
		<label for="password" class="form-control w-full max-w-xs">
			<div class="label">
				<span class="label-text">Password</span>
			</div>
			<input type="password" class="input input-bordered w-full max-w-xs" bind:value={password} />
		</label>
	</form>
	<button on:click|preventDefault={submit} class="btn btn-primary my-3">Login</button>
	<a href="/register" use:link class="btn btn-link">Register</a>
</main>
