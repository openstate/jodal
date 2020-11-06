<script>
import Entry from './Entry.svelte';
import VirtualList from '@sveltejs/svelte-virtual-list';
import IconButton from '@smui/icon-button';
import Textfield from '@smui/textfield'
import { sources } from '../stores.js';
import Switch from '@smui/switch';
import FormField from '@smui/form-field';
import { slide } from 'svelte/transition';

export let inquiry;

let start=0;
let end=5;
let selected = false;

let items = [];
let empty = false;
let query = "de";
let show_settings = false;

function doSomething() {
   show_settings = !show_settings;
 }

 console.dir(inquiry);
</script>

<section class="column-section">
<div class="column">
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
  <VirtualList items={$inquiry.entries} bind:start bind:end let:item>
  	<Entry {...item}/>
  </VirtualList>
  <p>showing items {start}-{end}</p>
  </div>
</div>
</section>

<style>
</style>
