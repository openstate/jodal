{#if showMsg}
<div class="message" bind:this={msg} in:fade out:fade>
<span>Dit is een test bericht. <a href="http://openstate.eu/" target="_blank">Meer &gt;</a></span>
<IconButton class="material-icons close-btn" aria-label="Sluiten" on:click={() => showMsg = false } title="Sluiten">close</IconButton>
</div>
{/if}

<script>
import IconButton from '@smui/icon-button';
import { fade } from 'svelte/transition';

let showMsg = true;;
let msg;
</script>

<style>
</style>
