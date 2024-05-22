<svelte:head>
  <title>Bron - alle overheidsdata — monitor, filter, stuur door</title>
</svelte:head>

<Router url="{url}">
<div class="app-container">
<Menu/>
<Drawer/>
<Route path="/">
  <Workspace/>
  <Fetcher/>
  <SearchHelp/>
  <Subscribe/>
</Route>
<Route path="bronnen" component="{Bronnen}" />
<Route path="over" component="{Over}" />
<Route path="login" component="{Login}"/>
<Route path="/d/:id" component={Doc} />
<Route path="/r/:id" component={Redirect} />
<Route path="/u/:user_id/:query_id" component={Unsubscribe} />

</div>
</Router>
<Document/>
<LoginDialog/>
<script>
  import { Router, Route, Link } from "svelte-routing";
  import Bronnen from "./pages/Bronnen.svelte";
  import Over from "./pages/Over.svelte";
  import Doc from './Doc.svelte';
  import Redirect from './Redirect.svelte';
  import Unsubscribe from './Unsubscribe.svelte';
  import Login from './Login.svelte';

  export let url = ""; //This property is necessary declare to avoid ignore the Router


	import Menu from './Menu.svelte';
	import Drawer from './Drawer.svelte';
  import Workspace from './Workspace.svelte';
  import Fetcher from './Fetcher.svelte';
  import Document from './Document.svelte';
  import SearchHelp from './SearchHelp.svelte';
  import Subscribe from './Subscribe.svelte';
  import LoginDialog from './LoginDialog.svelte';
  import { isTesting } from './stores.js';
  const runEnv = runEnvironment.env.isProd ? 'Production' : 'Dev';
  $: testEnv = $isTesting ? 'Test' : 'Beta';
</script>

<style>
</style>
