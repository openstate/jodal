<div class="workspace" id="workspace">
  <div class="columns">
    {#each $inquiries as col}
    	<Column name={col.name}/>
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
