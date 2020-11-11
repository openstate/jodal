<script>
export let title;
export let key;
export let date;
export let type;
export let column;
let empty = false;

import { slide } from 'svelte/transition';

</script>

<div class="entry" id="entry_{column}{key}" transition:slide="{{ duration: 150 }}">
  <div class="entry-title">
    <h4>{ title }</h4>
  </div>
  <div class="entry-contents">
  Lorem ipsum Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit
  </div>
  <div class="entry-byline">
  { date }
  { type }
  </div>
  <div class="entry-actions">

  </div>
</div>


<style>
</style>
