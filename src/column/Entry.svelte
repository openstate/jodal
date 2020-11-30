<script>
export let title;
export let key;
export let date;
export let type;
export let column;
export let description;
export let source;
let empty = false;

import { slide } from 'svelte/transition';

</script>

<div class="entry" id="entry_{column}{key}" transition:slide="{{ duration: 150 }}">
  {#if title}
  <div class="entry-title">
    <h4>{ title }</h4>
  </div>
  {/if}
  <div class="entry-contents">
  { @html description }
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
