<svelte:head>
  <title>Jodal</title>
</svelte:head>

<div class="app-container">
<Menu/>
<Drawer/>
<Workspace/>
<Fetcher/>
</div>

<script>
	import Menu from './Menu.svelte';
	import Drawer from './Drawer.svelte';
  import Workspace from './Workspace.svelte';
  import Fetcher from './Fetcher.svelte';
</script>

<style>
</style>
