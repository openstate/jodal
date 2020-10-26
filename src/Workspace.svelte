<div class="workspace" id="workspace">
  <div class="columns">
    {#each columns as col}
    	<Column name={col.name}/>
    {/each}
  </div>
</div>

<script>
import Column from './column/Column.svelte';
let empty = false;
let columns = [
  {name: 'Amsterdam'},
  {name: 'Groningen'},
];
</script>

<style>
</style>
