<h1>Inloggen</h1>

<script>
import { onMount, onDestroy } from 'svelte';
import { showLoginDialog } from './LoginDialog.svelte';

export let id = "";

$: if(id != "") { id="gelukt"; /*showLoginDialog()*/ }

onMount(function () {
  console.log('login onMount');
  id = "test";
  showLoginDialog();
});

onDestroy(function () {
});

</script>
