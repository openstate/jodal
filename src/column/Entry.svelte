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

function timeSince(now, timeStamp) {
  //var now = new Date();
  var secondsPast = (now.getTime() - timeStamp) / 1000;
  if (secondsPast < 60) {
    return parseInt(secondsPast) + 's';
  }
  if (secondsPast < 3600) {
    return parseInt(secondsPast / 60) + 'm';
  }
  if (secondsPast <= 86400) {
    return parseInt(secondsPast / 3600) + 'h';
  }
  if (secondsPast > 86400) {
    var tsDate = new Date(timeStamp);
    var day = tsDate.getDate();
    var month = tsDate.toDateString().match(/ [a-zA-Z]*/)[0].replace(" ", "");
    var year = tsDate.getFullYear() == now.getFullYear() ? "" : " " + tsDate.getFullYear();
    return day + " " + month + year  + " " + tsDate.toLocaleTimeString('nl-NL').slice(0,5);
  }
}

let cur_date = new Date();

function updateTime() {
  cur_date = new Date();
  setTimeout(updateTime, 10000);
}

$: time_since = timeSince(cur_date, Date.parse(date));

// lifecycle functions
onMount(() => {
  updateTime();
});
</script>

<div class="entry" id="entry_{column}{key}" transition:slide="{{ duration: 150 }}">
  {#if title}
  <div class="entry-title">
    <h4>
      <a href="#entry_{column}{key}" {title} on:click={function (e) { e.preventDefault(); showDocumentDialog(entry); return false;}}>
      { title }
      </a>
    </h4>
  </div>
  {/if}
  <div class="entry-contents">
    <a href="#entry_{column}{key}" class="entry-contents-link" {title} on:click={function (e) { e.preventDefault(); showDocumentDialog(entry); return false;}}>
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
        <a href="{ url }" target="_blank" title="{ source }" class="source-link">
          <img src="/images/sources/{ source }.svg" alt="{ source }" class="source-logo">
        </a>
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
