<script>
	import { Router, Link, Route } from 'svelte-routing';

	import Login from './lib/pages/login.svelte';
	import Home from './lib/pages/home.svelte';
	import Register from './lib/pages/register.svelte';
	import Logout from './lib/pages/logout.svelte';
	import Annotate from './lib/pages/annotate.svelte';

	export let url = '';
</script>

<Router {url}>
	<Route path="/annotate/:datum" let:params>
		<Annotate datum={params.datum} />
	</Route>
	<Route path="/login" component={Login} />
	<Route path="/register" component={Register} />
	<Route path="/logout" component={Logout} />
	<Route path="/" component={Home} />
</Router>

<style></style>
