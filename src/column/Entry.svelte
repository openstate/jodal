<script>
export let title;
export let key;
export let date;
export let type;
export let column;
export let description;
export let source;
export let url;

let empty = false;

import { slide } from 'svelte/transition';

</script>

<div class="entry" id="entry_{column}{key}" transition:slide="{{ duration: 150 }}">
  {#if title}
  <div class="entry-title">
    <h4>
      <a href="{ url }" target="_blank">
      { title }
      </a>
    </h4>
  </div>
  {/if}
  <div class="entry-contents">
  { @html description }
  </div>
  <div class="entry-byline">
  { date }
  { type }
  <a href="{ url }" target="_blank">
  { source }
  </a>
  </div>
  <div class="entry-actions">

  </div>
</div>


<style>
</style>
