<script>
import { onMount, onDestroy } from 'svelte';
import Entry from './Entry.svelte';
import Button from '@smui/button';
import IconButton from '@smui/icon-button';
import Textfield from '@smui/textfield'
import { writable, get, derived } from 'svelte/store';
import { sources, locations, fetchingEnabled, removeInquiry } from '../stores.js';
import { fetchSource } from '../sources.js';
import Switch from '@smui/switch';
import FormField from '@smui/form-field';
import { slide } from 'svelte/transition';
import Fab, {Label, Icon} from '@smui/fab';
import orderBy from 'lodash/orderBy';

export let inquiry;

let column_locations = [];
let last_length=0;
let start=0;
let end=5;
let selected = false;

let items_ = writable([]);
let items = derived(items_, (items_) => orderBy(items_, ['date'], ['desc']))
let item_ids = {};
let empty = false;
let query = inquiry.user_query;
let column_id = inquiry.id;
let show_settings = false;
let show_marker = false;
let scroll_marker;
let virtual_list;
let show_sources = false;

function getLocations() {
  column_locations = $locations.filter((l) => inquiry.locations.includes(l.id));
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
  console.log('toggling settings!');
   show_settings = !show_settings;
 }

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

function removeColumn() {
  removeInquiry(column_id);
}

var interval;


onMount(function () {
  async function fetchData() {
    if (get(fetchingEnabled)) {

      if (column_locations.length <= 0) {
        getLocations();
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
      // FIXME: sources are fetched in parralel so updating the items does not work correctly like this.
      // so we wait until the full batch is complete then compare and update items
      $sources.forEach(function (s) {
          fetchSource(inquiry.user_query, s.short, locations2sources[s.short], function (fetched_items) {
            console.log('should set items now!');
            var real_items = get(items_);
            fetched_items.reverse();
            fetched_items.forEach(function (i) {
              if (typeof(item_ids[i.key]) === 'undefined') {
                real_items.unshift(i);
                item_ids[i.key] = 1;
              }
            });
            items_.set(real_items);
          });
      });
      // var entry_idx = $items.length + 10;
      // var default_new_entry = {
      //   'key': "_" + entry_idx,
      //   'title': 'Raadscommissie Kunst Diversiteit ' + entry_idx,
      //   'type': 'Vergadering',
      //   'source': 'https://openbesluitvorming.nl/',
      //   'date': '11-11-2020',
      //   'time': '13:30'
      // };
      clearInterval(interval);
      interval = setInterval(fetchData, 60000 + (inquiry.order * 1000) + (Math.random() * 2000));
    } else {
      //console.log('Fetching not yet enabled for column ' + inquiry.name);
    }
  };
  interval = setInterval(fetchData, 1000 + (Math.random() * 2000));
  fetchData();
});

onDestroy(function () {
  clearInterval(interval);
});

</script>

<svelte:window on:focus={getFocus} on:blur={loseFocus} />

<section class="column-section">
<div id="column-{column_id}" class="column">
  <div class="column-title">
    <h2>{ inquiry.name }</h2>
    <IconButton align="end" class="material-icons" aria-label="Instellingen" alt="Instellingen" on:click={() => doSomething()}>tune</IconButton>
  </div>
  {#if show_settings}
  <div class="column-settings" class:active={show_settings} transition:slide="{{ duration: 500 }}">
    <Textfield bind:value={query} label="Query" />
    {#if show_sources}
      {#each $sources as src}
      <FormField>
        <Switch bind:checked={selected} />
        <span slot="label">{ src.name }</span>
      </FormField>
      {/each}
    {/if}
    <div class="column-settings-actions">
      <Button align="end" on:click={() => removeColumn()}><Label>Kolom verwijderen</Label></Button>
    </div>
  </div>
  {/if}
  <div id="column-contents-{column_id}" class="column-contents">
  {#if show_marker}
    <Fab on:click={doGoToEntry} extended><Label>Nieuwe entries!</Label></Fab>
  {/if}
  {#each $items as entry}
  	<Entry {...entry} column={column_id} />
  {/each}
  </div>
</div>
</section>

<style>
</style>
