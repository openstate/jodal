<svelte:head>
  <title>Open Overheidsdata {testEnv}</title>
</svelte:head>

<Router url="{url}">
<div class="app-container">
<Menu/>
<Drawer/>
<Route path="/">
  <Workspace/>
  <Fetcher/>
  <Document/>
  <SearchHelp/>
  <Subscribe/>
</Route>
<Route path="bronnen" component="{Bronnen}" />
<Route path="over" component="{Over}" />
</div>
</Router>

<script>
  import { Router, Route, Link } from "svelte-routing";
  import Bronnen from "./pages/Bronnen.svelte";
  import Over from "./pages/Over.svelte";
  export let url = ""; //This property is necessary declare to avoid ignore the Router


	import Menu from './Menu.svelte';
	import Drawer from './Drawer.svelte';
  import Workspace from './Workspace.svelte';
  import Fetcher from './Fetcher.svelte';
  import Document from './Document.svelte';
  import SearchHelp from './SearchHelp.svelte';
  import Subscribe from './Subscribe.svelte';
  import { isTesting } from './stores.js';
  const runEnv = runEnvironment.env.isProd ? 'Production' : 'Dev';
  $: testEnv = $isTesting ? 'Test' : 'Beta';
</script>

<style>
</style>
