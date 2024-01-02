<script>
export let title = "(zonder titel)";
export let key;
export let date;
export let type;
export let column;
export let description;
export let highlight;
export let source;
export let url;
export let location;
export let entry;

let empty = false;

import { slide } from 'svelte/transition';
import { onMount, onDestroy } from 'svelte';
import { showDocumentDialog } from '../Document.svelte';

function timeDisplay(timeStamp) {
  var tsDate = new Date(timeStamp);
  var day = tsDate.getDate();
  var month = tsDate.toDateString().match(/ [a-zA-Z]*/)[0].replace(" ", "");
  var year = " " + tsDate.getFullYear();
  return day + " " + month + year; //  + " " + tsDate.toLocaleTimeString('nl-NL').slice(0,5);
}

let cur_date = Date.parse(date);

$: time_since = timeDisplay(cur_date);

</script>

<div class="entry" id="entry_{column}{key}" transition:slide="{{ duration: 150 }}" on:click={function (e) { e.preventDefault(); showDocumentDialog(entry); return false;}}>
  <div class="entry-title">
  {#if title}
    <a href="#entry_{column}{key}" {title}>
    { title }
    </a>
  {:else}
  <a href="#entry_{column}{key}">
  ( zonder titel )
  </a>
  {/if}
    <div class="entry-date">{time_since}</div>
  </div>
</div>


<style>
</style>
