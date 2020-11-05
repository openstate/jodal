<script>
import Entry from './Entry.svelte';
import VirtualList from '@sveltejs/svelte-virtual-list';
import IconButton from '@smui/icon-button';
import Textfield from '@smui/textfield'
import { sources } from '../stores.js';
import Switch from '@smui/switch';
import FormField from '@smui/form-field';
import { slide } from 'svelte/transition';

export let name;
let start=0;
let end=5;
let selected = false;

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
let query = "de";
let show_settings = false;

console.dir(items);

function doSomething() {
   show_settings = !show_settings;
 }
</script>

<section class="column-section">
<div class="column">
  <div class="column-title">
    <h2>{ name }</h2>
    <IconButton align="end" class="material-icons" aria-label="Bookmark this page" on:click={doSomething}>filter_alt</IconButton>
  </div>
  {#if show_settings}
  <div class="column-settings" class:active={show_settings} transition:slide="{{ duration: 500 }}">
    <Textfield bind:value={query} label="Query" />
    {#each $sources as src}
    <FormField>
      <Switch bind:checked={selected} />
      <span slot="label">{ src.name }</span>
    </FormField>
    {/each}
  </div>
  {/if}
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
