<svelte:head>
  <title>Journalistiek Dashboard Lokaal - Beta ({runEnv})</title>
</svelte:head>

<div class="app-container">
<Menu/>
<Drawer/>
<Workspace/>
<Fetcher/>
<Document/>
</div>

<script>
	import Menu from './Menu.svelte';
	import Drawer from './Drawer.svelte';
  import Workspace from './Workspace.svelte';
  import Fetcher from './Fetcher.svelte';
  import Document from './Document.svelte';

  const runEnv = runEnvironment.env.isProd ? 'Production' : 'Dev';
</script>

<style>
</style>
