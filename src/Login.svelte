<h1>Inloggen</h1>

{#if !$loginDialogOpen}
<p>Er is zojuis een e-mail naar het opgegeven adres gestuurd met verdere instructies om in te loggen. U kunt dit venster nu sluiten.</p>
{/if}

<script>
import { onMount, onDestroy } from 'svelte';
import { showLoginDialog } from './LoginDialog.svelte';
import { loginDialogOpen } from './stores.js';

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
