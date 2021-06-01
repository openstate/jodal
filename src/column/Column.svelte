<script>
import { onMount, onDestroy } from 'svelte';
import Entry from './Entry.svelte';
import Button from '@smui/button';
import IconButton from '@smui/icon-button';
import Textfield from '@smui/textfield'
import { writable, get, derived } from 'svelte/store';
import { sources, locations, inquiries, fetchingEnabled, removeInquiry } from '../stores.js';
import { fetchSource } from '../sources.js';
import Checkbox from '@smui/checkbox';
import FormField from '@smui/form-field';
import { fade, slide } from 'svelte/transition';
import Fab, {Label, Icon} from '@smui/fab';
import orderBy from 'lodash/orderBy';
import { showDocumentDialog } from '../Document.svelte';

export let inquiry;

let column_locations = [];
let last_length=0;
let start=0;
let end=5;
let selected = [];

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
let show_sources = true;
let loading = true;
let hidden = false;
let stable_date = undefined;
let stable_page_number = 1;
let old_source_counts = writable({});
let source_counts = writable({});

function getLocations() {
  column_locations = $locations.filter((l) => inquiry.locations.includes(l.id));
  $sources.forEach(function (s) {
    if (inquiry['src_' + s.short]) {
      selected.push(s.short);
    }
  });
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

function doNextPage() {
  console.log('should get next page with stable ' + stable_date + ' with page ' + stable_page_number);
  loading = true;
  fetchFromSources(stable_page_number, stable_date);
  stable_page_number += 1;
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
  old_source_counts.set(source_counts);
}

function handleClosedLeading() {
  console('leadgsackar closed');
}

function removeColumn() {
  show_settings = false;
  hidden = true;
  removeInquiry(column_id);
}

function handleQueryInput(e){
    // console.log('new query input should be handled!:');
    // console.dir(e);
}

function handleQueryChange(e){
    console.log('new query change should be handled!:');
    console.dir(e);
    items_.set([]);
    item_ids = {};
    inquiry.user_query = query;

    $sources.forEach(function (s) {
      var val = (selected.indexOf(s.short) >= 0) ? true : false;
      inquiry['src_' + s.short] = val;
    });

    var url = window.location.protocol + '//api.jodal.nl/columns/' + inquiry.id;
    fetch(
      url, {
        method: 'POST',
        credentials: 'include',
        cache: 'no-cache',
        body: JSON.stringify(inquiry),
        headers: new Headers({'content-type': 'application/json'})
      }).then(
        response => response.json()
      ).then(
        function (data) {
            console.log('update of column completed:');
            console.dir(data);
        }
    );
    var old_inquiries = get(inquiries).map(function (i) {
      if ((i.order == inquiry.order) && (i.user_query == inquiry.user_query)){
        return inquiry;
      } else {
        return i;
      }
    });
    inquiries.set(old_inquiries);
    show_settings = !show_settings;
    loading = true;
    console.log('fetchting for query change!');
    fetchFromSources();
}

function fetchFromSources(page, stable_param) {
  var real_page = 0;
  if (typeof(page) !== 'undefined') {
    real_page = page;
  }
  var real_stable = null;
  if (typeof(stable_param) !== 'undefined') {
    real_stable = stable_param;
  }
  if (column_locations.length <= 0) {
    getLocations();
  }

  console.log('should fetch data for colum ' + inquiry.name + ' now!!');
  var selected_sources = []
  $sources.forEach(function (s) {
    if (selected.indexOf(s.short) >= 0) {
      selected_sources.push(s.short);
    } else {
      console.log('Source ' + s.short + ' not fetched because not selected.');
    }
  });
  console.log('fetching ' + selected_sources + ' now ...');

  fetchSource(inquiry.user_query, selected_sources, column_locations, real_stable, real_page, function (fetched_items, original_response) {
    console.log('should set items now!');
    var real_items = get(items_);
    fetched_items.reverse();
    if ((typeof(stable_date) === 'undefined') && (fetched_items.length > 0)) {
      stable_date = fetched_items[0].date;
      console.log('Set stable date for column ' + inquiry.name + 'sorting to: ' + stable_date);
    }
    fetched_items.forEach(function (i) {
      if (typeof(item_ids[i.key]) === 'undefined') {
        real_items.unshift(i);
        item_ids[i.key] = 1;
      }
    });

    var new_source_counts = {};
    original_response.aggregations.source.buckets.forEach(function (b) {
      new_source_counts[b.key] = b.doc_count;
    });
    console.log('new counts:');
    console.dir(new_source_counts);

    items_.set(real_items);
    source_counts.set(new_source_counts);
    loading = false;
  });

}

// https://ourcodeworld.com/articles/read/713/converting-bytes-to-human-readable-values-kb-mb-gb-tb-pb-eb-zb-yb-with-javascript
function human_readable_numer(numb) {
    if (numb > 0) {
      var base = 1000;
      var i = Math.floor(Math.log(numb) / Math.log(base)),
      sizes = ['', 'K', 'M', 'm', 'B', '', '', '', ''];

      return (numb / Math.pow(base, i)).toFixed(1) * 1 + '' + sizes[i];
    } else {
      return '0';
    }
}

var interval;


onMount(function () {
  async function fetchData() {
    if (get(fetchingEnabled) && !hidden) {

      fetchFromSources();

      clearInterval(interval);
      interval = setInterval(fetchData, 60000 + (inquiry.order * 1000) + (Math.random() * 2000));
    } else {
      console.log('Fetching not yet enabled for column ' + inquiry.name);
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

{#if !hidden}
<section class="column-section" out:fade>
<div id="column-{column_id}" class="column">
  <div class="column-title">
    <h2>{ inquiry.name }</h2>
    <IconButton align="end" class="material-icons" aria-label="Instellingen" alt="Instellingen" on:click={() => doSomething()}>tune</IconButton>
  </div>
  {#if show_settings}
  <div class="column-settings" class:active={show_settings} transition:slide="{{ duration: 500 }}">
    <Textfield bind:value={query} on:change={handleQueryChange} on:input={handleQueryInput} label="Query" />
    {#if show_sources}
      {#each $sources as src}
      <div>
      <FormField>
        <Checkbox bind:group={selected} value={src.short} />
        <span slot="label">{ src.name }</span>
      </FormField>
      </div>
      {/each}
    {/if}
    <div class="column-settings-actions">
      <Button align="begin" variant="unelevated" on:click={() => handleQueryChange()}><Label>Wijzigen</Label></Button>
      <Button align="end" variant="outlined" on:click={() => removeColumn()}><Label>Verwijderen</Label></Button>
    </div>
  </div>
  {/if}
  {#if $items.length > 0}
  <div class="column-counts">
    {#each $sources as s}
      <div class="column-counts-source">
        <img src="/images/sources/{ s.short }.svg" alt="{ s.name }" title="{s.name}" class="source-logo"><span title="{$source_counts[s.short] || 0}">{human_readable_numer($source_counts[s.short] || 0)}</span>
      </div>
    {/each}
  </div>
  {/if}
  <div id="column-contents-{column_id}" class="column-contents">
  {#if !loading && ($items.length <= 0)}
    <p>Er werd nog niks gevonden dat aan je zoekopdracht voldeed.</p>
  {/if}
  {#if show_marker}
    <Fab on:click={doGoToEntry} extended><Label>Nieuwe entries!</Label></Fab>
  {/if}
  {#each $items as entry}
  	<Entry {...entry} column={column_id} entry={entry} />
  {/each}
  {#if !loading && ($items.length > 0)}
  <div id="more-page-link" class="entry entry-paging">
    <Button variant="outlined" on:click={() => doNextPage()}><Label>Meer resultaten</Label></Button>
  </div>
  {/if}
  {#if loading}
    <div class="loading"></div>
  {/if}
  </div>
</div>
</section>
{/if}

<style>
</style>
