<div class="workspace" id="workspace">
  <div class="columns">
  {#if $identity}
    {#if $inquiries.length <= 0}
    <div class="start-explainer">
      <p>Je hebt nog geen zoekopdracht toegevoegd. Klik op de knop hieronder om er een toe te voegen.</p>
      <Button align="end" on:click={() => startAddColumn()}><Label>Zoekopdracht toevoegen</Label></Button>
    </div>
    {/if}
    {#each $inquiries as inq}
    	<Column inquiry={inq} />
    {/each}
  {:else}
  <div class="start-explainer">
    <p>Je bent niet ingelogd. Klik op de knop hieronder om in te loggen of een account aan te maken.</p>
    <Button align="end" href="//api.jodal.nl/users/simple/login"><Label>Inloggen</Label></Button>
  </div>
  {/if}
  </div>
</div>

<script>
import { inquiries, identity } from './stores.js';
import Column from './column/Column.svelte';
import AddColumn, { startAddColumn } from './AddColumn.svelte';
import Button from '@smui/button';
import Fab, {Label, Icon} from '@smui/fab';

let empty = ($inquiries.length <= 0);
</script>

<style>
</style>
