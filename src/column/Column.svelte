<section class="column-section">
<div class="column">
  <div calss="column-title">
    <h1>{ name }</h1>
  </div>
  <div class="column-contents">
  {#each entries as entry}
  	<Entry entry={entry}/>
  {/each}
  </div>
</div>
</section>

<script>
import Entry from './Entry.svelte';

export let name;
let entries = [
  {
    'title': 'Vergadering 26-10-2020'
  },
  {
    'title': 'Vergadering 26-09-2020'
  },
  {
    'title': 'Vergadering 26-08-2020'
  },
  {
    'title': 'Vergadering 26-07-2020'
  },
  {
    'title': 'Vergadering 26-06-2020'
  },
  {
    'title': 'Vergadering 26-05-2020'
  },
  {
    'title': 'Vergadering 26-04-2020'
  }
]
let empty = false;
</script>

<style>
</style>
