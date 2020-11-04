<script>
import Entry from './Entry.svelte';
import VirtualList from '@sveltejs/svelte-virtual-list';
import IconButton from '@smui/icon-button';

export let name;
let start=0;
let end=5;

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

let items = shuffle([
  {
    'key': "_3",
    'title': 'Raadscommissie Kunst Diversiteit en Democratisering',
    'type': 'Vergadering',
    'source': 'https://openbesluitvorming.nl/',
    'date': '11-11-2020',
    'time': '13:30'
  },
  {
    'key': "_2",
    'title': 'Deze vergadering vindt digitaal plaats. Insprekers kunnen digitaal inspreken',
    'type': 'Agendapunt',
    'source': 'https://openbesluitvorming.nl/',
    'date': '11-11-2020',
    'time': '12:45'
  },
  {
    'key': "_3",
    'title': 'Commissie Agenda (Definitieve)',
    'type': 'Document',
    'source': 'https://openbesluitvorming.nl/',
    'date': '11-11-2020',
    'time': '12:45'
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
]);
let empty = false;

console.dir(items);
</script>

<section class="column-section">
<div class="column">
  <div class="column-title">
    <h2>{ name }</h2>
    <IconButton align="end" class="material-icons" aria-label="Bookmark this page">filter_alt</IconButton>
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
