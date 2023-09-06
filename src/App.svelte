<svelte:head>
  <title>Open Overheidsdata {testEnv}</title>
</svelte:head>

<Router url="{url}">
<div class="app-container">
<Route path="/">
  <Menu/>
  <Drawer/>
  <Workspace/>
  <Fetcher/>
  <Document/>
  <SearchHelp/>
  <Subscribe/>
</Route>
</div>
</Router>

<script>
  import { Router, Route, Link } from "svelte-routing";
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
