<script>
import Entry from './Entry.svelte';
import VirtualList from '@sveltejs/svelte-virtual-list';
import IconButton from '@smui/icon-button';
import Textfield from '@smui/textfield'
import { sources } from '../stores.js';
import Switch from '@smui/switch';
import FormField from '@smui/form-field';
import { slide } from 'svelte/transition';
import Fab, {Label, Icon} from '@smui/fab';
export let inquiry;

let last_length=0;
let start=0;
let end=5;
let selected = false;

let items = [];
let empty = false;
let query = "de";
let show_settings = false;
let show_marker = false;
let scroll_marker;
let virtual_list;

function doSomething() {
   show_settings = !show_settings;
 }

function doGoToEntry() {
  show_marker = false;
  if (scroll_marker) {
    var entry_name = 'entry_' + $inquiry.order + scroll_marker;
    console.log(entry_name);
    var myElement = document.getElementById(entry_name);
    // var topPos = myElement.offsetTop;
    // console.log('Should move column ' + $inquiry.order + 'to position ' + topPos + 'now!');
    console.dir(virtual_list);
  }
}

function getFocus() {
  var count = $inquiry.entries.length;
  console.log('got focus! resulted in  ' + (count - last_length) + ' new items');
  last_length = 0;
  show_marker =  ((count-last_length) > 0); //(end - start);
  last_length = count;
}

function loseFocus() {
  var count = $inquiry.entries.length;
  //scroll_marker = virtual_list.items[start];
  console.log('Lost focus in column ' + $inquiry.order + '!: ' + $inquiry.entries[start].key);
  scroll_marker = $inquiry.entries[start].key;
  last_length = count;
  show_marker = false;
}

function handleClosedLeading() {
  console('leadgsackar closed');
}
</script>

<svelte:window on:focus={getFocus} on:blur={loseFocus} />

<section class="column-section">
<div id="column-{$inquiry.order}" class="column">
  <div class="column-title">
    <h2>{ $inquiry.name }</h2>
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
  {#if show_marker}
    <Fab on:click={doGoToEntry} extended><Label>Nieuwe entries!</Label></Fab>
  {/if}
  <VirtualList items={$inquiry.entries} bind:this={virtual_list} bind:start bind:end let:item>
  	<Entry {...item} column={$inquiry.order} />
  </VirtualList>
  <p>showing items {start}-{end}</p>
  </div>
</div>
</section>

<style>
</style>
