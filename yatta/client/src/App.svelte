<script>
	import { user } from './lib/stores';
	import { Router, Link, Route, link } from 'svelte-routing';

	import Login from './lib/pages/login.svelte';
	import Home from './lib/pages/home.svelte';
	import Register from './lib/pages/register.svelte';
	import Logout from './lib/pages/logout.svelte';
	import Annotate from './lib/pages/annotate.svelte';

	export let url = '';
</script>

<Router {url}>
	<nav class="navbar bg-accent">
		<div class="flex-none text-xl"><b>🍃 yatta</b></div>
		<div class="flex-1"></div>
		{#if $user}
			<ul class="menu menu-horizontal">
				<!-- <li>
					<input
						type="number"
						placeholder="Go to item..."
						class="input input-bordered w-32 input-sm"
					/>
				</li> -->
				<li>
					<a href="/" use:link>Home</a>
				</li>
				<li>
					<a href="/logout" use:link>Logout</a>
				</li>
			</ul>
    {:else}
      <ul class="menu menu-horizontal">
        <li>
          <a href="/login" use:link>Login</a>
        </li>
      </ul>
		{/if}
		<!-- <div class="flex-none menu menu-horizontal">
		</div> -->
	</nav>
	<div class="max-w-screen-md mx-auto">
		<Route path="/annotate/:datum" let:params>
			<Annotate datum={params.datum} />
		</Route>
		<Route path="/login" component={Login} />
		<Route path="/register" component={Register} />
		<Route path="/logout" component={Logout} />
		<Route path="/" component={Home} />
	</div>
</Router>

<style>
</style>
