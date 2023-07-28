<svelte:head>
  <title>Open Overheidsdata</title>
</svelte:head>

<div class="app-container">
<Menu/>
<AddColumnBar/>
<Drawer/>
<Workspace/>
<Fetcher/>
<Document/>
<SearchHelp/>
</div>

<script>
	import Menu from './Menu.svelte';
	import Drawer from './Drawer.svelte';
  import Workspace from './Workspace.svelte';
  import Fetcher from './Fetcher.svelte';
  import Document from './Document.svelte';
  import SearchHelp from './SearchHelp.svelte';
  import AddColumnBar from './AddColumnBar.svelte';
  import { isTesting } from './stores.js';
  const runEnv = runEnvironment.env.isProd ? 'Production' : 'Dev';
  $: testEnv = $isTesting ? 'Test' : 'Beta';
</script>

<style>
</style>
