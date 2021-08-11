<script>
export let title;
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
  return day + " " + month + year  + " " + tsDate.toLocaleTimeString('nl-NL').slice(0,5);
}

let cur_date = Date.parse(date);

$: time_since = timeDisplay(cur_date);

</script>

<div class="entry" id="entry_{column}{key}" transition:slide="{{ duration: 150 }}" on:click={function (e) { e.preventDefault(); showDocumentDialog(entry); return false;}}>
  {#if title}
  <div class="entry-title">
    <h4>
      <a href="#entry_{column}{key}" {title}>
      { title }
      </a>
    </h4>
  </div>
  {/if}
  <div class="entry-contents">
    <a href="#entry_{column}{key}" class="entry-contents-link" {title}>
    { @html highlight }
    </a>
  </div>
  <div class="entry-byline">
    <ul>
    <li>
      <date title="{ date }">{ time_since }</date>
    </li>
    <li class="last">
    <strong>{ location }</strong>
    </li>
    </ul>
    <ul>
      <li class="first">
        <div class="source-link">
          <img src="/images/sources/{ source }.svg" alt="{ source }" class="source-logo">
        </div>
      </li>
      <li class="last">
        { type }
      </li>
    </ul>
  </div>
  <div class="entry-actions">

  </div>
</div>


<style>
</style>
