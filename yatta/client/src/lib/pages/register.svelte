<script>
	import { Link, navigate } from 'svelte-routing';
	import { register } from '../api';

	let first_name = '';
	let last_name = '';
	let username = '';
	let password = '';
	let error = null;

	const submit = async () => {
		const { success } = await register(first_name, last_name, username, password);
		if (success) navigate('/login');
		error = 'Something went wrong!';
	};
</script>

<main>
	<form>
		<label for="first_name" class="form-control w-full max-w-xs">
			<div class="label">
				<span class="label-text">First Name</span>
			</div>
			<input type="text" class="input input-bordered w-full max-w-xs" bind:value={first_name} />
		</label>
		<label for="last_name" class="form-control w-full max-w-xs">
			<div class="label">
				<span class="label-text">Last Name</span>
			</div>
			<input type="text" class="input input-bordered w-full max-w-xs" bind:value={last_name} />
		</label>
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
	<button on:click|preventDefault={submit} class="btn btn-primary my-3">Create account</button>
	<a href="/login" class="btn btn-link">Log in instead</a>
</main>
