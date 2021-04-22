<svelte:head>
  <title>Journalistiek Dashboard Lokaal - Beta</title>
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
</script>

<style>
</style>
