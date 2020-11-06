<div class="workspace" id="workspace">
  <div class="columns">
    {#each $inquiries as inq}
    	<Column inquiry={inq} />
    {/each}
  </div>
</div>

<script>
import { inquiries } from './stores.js';
import Column from './column/Column.svelte';
let empty = false;
</script>

<style>
</style>
