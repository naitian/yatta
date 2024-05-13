<script>
	import Page from '$lib/components/Page.svelte';
	import Input from '$lib/components/ui/input/input.svelte';
	import Label from '$lib/components/ui/label/label.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
</script>

<Page title="Register">
	<form>
		<div class="flex justify-between space-x-4">
			<div class="grow">
				<Label for="last">First Name</Label>
				<Input type="text" />
			</div>
			<div class="grow">
				<Label for="first">Last Name</Label>
				<Input type="text" />
			</div>
		</div>
		<div>
			<Label for="username">Username</Label>
			<Input type="text" />
		</div>
		<div>
			<Label for="password">Password</Label>
			<Input type="password" />
		</div>
		<div>
			<Button type="submit">Register</Button>
			<a href="/login"><Button variant="link">Log in instead</Button></a>
		</div>
	</form>
</Page>

<style>
	form {
		@apply flex max-w-md flex-col space-y-4;
	}
</style>
