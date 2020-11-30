<script>
import { onMount, onDestroy } from 'svelte';
import Entry from './Entry.svelte';
import IconButton from '@smui/icon-button';
import Textfield from '@smui/textfield'
import { writable, get } from 'svelte/store';
import { sources, locations, default_entries, fetchingEnabled } from '../stores.js';
import Switch from '@smui/switch';
import FormField from '@smui/form-field';
import { slide } from 'svelte/transition';
import Fab, {Label, Icon} from '@smui/fab';
export let inquiry;

let column_locations = [];
let last_length=0;
let start=0;
let end=5;
let selected = false;

let items = writable([]); //writable(shuffle(default_entries));
let empty = false;
let query = "de";
let show_settings = false;
let show_marker = false;
let scroll_marker;
let virtual_list;

function getLocations() {
  column_locations = $locations.filter((l) => inquiry.ids.includes(l.id));
  console.log('Get the following locations:');
  console.dir(column_locations);
}

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

  return array.map(function (i) {return i;});
}

function doSomething() {
   show_settings = !show_settings;
 }

function coumn_id() {
    return "column-" + inquiry.order;
};

function doGoToEntry() {
  show_marker = false;
  if (scroll_marker) {
    var column_id = "column-contents-" + inquiry.order;
    var entry_name = 'entry_' + inquiry.order + scroll_marker;
    //console.log(entry_name);
    var myElement = document.getElementById(entry_name);
    var topPos = myElement.offsetTop;
    console.log('entry ' + entry_name + ' is at ' + topPos);
    // console.log('Should move column ' + inquiry.order + 'to position ' + topPos + 'now!');
    document.getElementById(column_id).scrollTop = topPos;
  }
}

function getFocus() {
  var count = $items.length;
  console.log('got focus! resulted in  ' + (count - last_length) + ' new $items');
  last_length = 0;
  show_marker =  ((count-last_length) > 0); //(end - start);
  last_length = count;
}

function loseFocus() {
  var count = $items.length;
  //scroll_marker = virtual_list.$items[start];
  if (count > 0) {
    console.log('Lost focus in column ' + inquiry.order + '!: ' + $items[start].key);
    scroll_marker = $items[start].key;
    last_length = count;
    show_marker = false;
  }
}

function handleClosedLeading() {
  console('leadgsackar closed');
}

var interval;

onMount(function () {
  console.log('Setting up fetch for colum:');
  console.dir(inquiry);
  async function fetchData() {
    if (get(fetchingEnabled)) {

      if (column_locations.length <= 0) {
        console.log('getting column locations');
        getLocations();
        console.log(column_locations);
      }

      console.log('should fetch data for colum ' + inquiry.name + ' now!!');
      var locations2sources = {};
      $sources.forEach(function (s) {
        locations2sources[s.short] = [];
      });
      column_locations.forEach(function (c) {
        c.sources.forEach(function (s) {
          //console.log('s:');
          //console.dir(s.source);
          locations2sources[s.source].push(s.id);
        })
      });
      console.log(locations2sources);
      // var entry_idx = $items.length + 10;
      // var default_new_entry = {
      //   'key': "_" + entry_idx,
      //   'title': 'Raadscommissie Kunst Diversiteit ' + entry_idx,
      //   'type': 'Vergadering',
      //   'source': 'https://openbesluitvorming.nl/',
      //   'date': '11-11-2020',
      //   'time': '13:30'
      // };

      // var real_items = get(items);
      // real_items.unshift(default_new_entry);
      // items.set(real_items);
    } else {
      console.log('Fetching not yet enabled for column ' + inquiry.name);
    }
  };
  interval = setInterval(fetchData, 5000 + (Math.random() * 2000));
  fetchData();
});

onDestroy(function () {
  clearInterval(interval);
});

</script>

<svelte:window on:focus={getFocus} on:blur={loseFocus} />

<section class="column-section">
<div id="column-{inquiry.order}" class="column">
  <div class="column-title">
    <h2>{ inquiry.name }</h2>
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
  <div id="column-contents-{inquiry.order}" class="column-contents">
  {#if show_marker}
    <Fab on:click={doGoToEntry} extended><Label>Nieuwe entries!</Label></Fab>
  {/if}
  {#each $items as entry}
  	<Entry {...entry} column={inquiry.order} />
  {/each}
  </div>
</div>
</section>

<style>
</style>
