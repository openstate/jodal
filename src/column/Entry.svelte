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

function timeSince(timeStamp) {
  var now = new Date();
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
    <ul>
      <li class="first">
        <a href="{ url }" target="_blank" title="{ source }" class="source-link">
          <img src="/images/sources/{ source }.svg" alt="{ source }" class="source-logo">
        </a>
      </li>
      <li>
        <date title="{ date }">{ timeSince(Date.parse(date)) }</date>
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
