<script>
import Entry from './Entry.svelte';
import VirtualList from '@sveltejs/svelte-virtual-list';

export let name;
let start=0;
let end=5;

let items = [
  {
    'key': "_1",
    'title': 'Vergadering 26-10-2020'
  },
  {
    'key': "_2",
    'title': 'Vergadering 26-09-2020'
  },
  {
    'key': "_3",
    'title': 'Vergadering 26-08-2020'
  },
  {
    'key': "_4",
    'title': 'Vergadering 26-07-2020'
  },
  {
    'key': "_5",
    'title': 'Vergadering 26-06-2020'
  },
  {
    'key': "_6",
    'title': 'Vergadering 26-05-2020'
  },
  {
    'key': "_7",
    'title': 'Vergadering 26-04-2020'
  }
];
let empty = false;

console.dir(items);
</script>

<section class="column-section">
<div class="column">
  <div class="column-title">
    <h1>{ name }</h1>
  </div>
  <div class="column-contents">
  <VirtualList {items} bind:start bind:end let:item>
  	<Entry {...item}/>
  </VirtualList>
  <p>showing items {start}-{end}</p>
  </div>
</div>
</section>

<style>
</style>
