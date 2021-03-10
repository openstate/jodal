<div class="workspace" id="workspace">
  <div class="columns">
  {#if $inquiries.length <= 0}
  <div class="start-explainer">
    <p>Je hebt nog geen kolommen toegevoegd. Klik op de knop hieronder om er een toe te voegen.</p>
    <Button align="end" on:click={() => startAddColumn()}><Label>Kolom toevoegen</Label></Button>
  </div>
  {/if}
    {#each $inquiries as inq}
    	<Column inquiry={inq} />
    {/each}
  </div>
</div>

<script>
import { inquiries } from './stores.js';
import Column from './column/Column.svelte';
import AddColumn, { startAddColumn } from './AddColumn.svelte';
import Button from '@smui/button';
import Fab, {Label, Icon} from '@smui/fab';

let empty = ($inquiries.length <= 0);
</script>

<style>
</style>
