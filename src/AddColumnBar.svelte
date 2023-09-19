<Modal>
  <div slot="modalTitle">Melding</div>
  <div slot="modalContent">Het aanmelden is gelukt. Je krijgt ook een mailtje hierover in je mailbox.</div>
</Modal>
<div class="sub-toolbar">
  <div class="flexy">
    <div class="cell cell-auto-flex bordered">
      <Icon class="material-icons">search</Icon>
      <input  bind:value={newQuery} id="column-query" aria-controls="helper-text-column-query" aria-describedby="helper-text-column-query" on:change={() => handleQueryChange()} on:blur={() => handleQueryChange()} on:keyup={() => handleWithTypeTimer()} />
    </div>
    <div class="cell cell-auto-flex bordered">
      <LocationSelector bind:selectedLocations showEmptyButton={false}/>
    </div>
  </div>
  <div class="flexy flexy-alt">
    <div class="cell bordered margined">
      <input bind:value={email} id="subscribe-email" placeholder="E-mail" />
    </div>
    <div class="cell">
      <Button class="subscribe-button" on:click={() => handleSubscription()}>Maak alert aan</Button>
    </div>
    <div class="cell">
    <a href="#" on:click={() => toggleAdvancedOptions()}>Meer opties
    </a>
    <Icon class="material-icons expand-more">{advancedChevron}</Icon>
    </div>
  </div>
  {#if showAdvancedOptions}
  <div class="flexy flexy-alt flexy-alt2"  transition:slide="{{ duration: 500 }}">
    <div class="cell cell-col">
    <h4>Bronnen</h4>
    <div class="flexy flexy-start">
    {#each $sources as s}
      <div class="checkbox-source">
      <input type="checkbox" id="source-checkbox-{s.short}" name="source"  bind:group={checkedSources} value="{s.short}" on:change={() => handleQueryChange()}><label for="source-checkbox-{s.short}">{s.name}</label>
      </div>
    {/each}
    </div>
    </div>
    <div class="cell cell-col">
      <h4>Frequentie</h4>
      <select bind:value={frequency}>
        <option value="" selected={frequency == ''}>Direct</option>
        <option value="1h" selected={frequency == '1h'}>Elk uur</option>
        <option value="24h" selected={frequency == '24h'}>Elke dag</option>
        <option value="168h" selected={frequency == '168h'}>Elke week</option>
      </select>
    </div>
  </div>
  {/if}
</div>
<script>
  import { addInquiry, removeInquiry, inquiries, locations, selectable_locations, id2locations, sources, drawerOpen,fetchingEnabled, identity, isTesting, apiDomainName, domainName, selected_inquiry, selected_inquiry_id } from './stores.js';
  import AddColumn, { startAddColumn } from './AddColumn.svelte';
  import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
  import IconButton from '@smui/icon-button';
  import Button from '@smui/button';
  import Checkbox from '@smui/checkbox';
  import Fab, {Label} from '@smui/fab';
  import { Icon} from '@smui/common';
  import FormField from '@smui/form-field';
  import Textfield, {Input, Textarea} from '@smui/textfield';
  import FloatingLabel from '@smui/floating-label';
  import LineRipple from '@smui/line-ripple';
  import HelperText from '@smui/textfield/helper-text/index';
  import Account, { showAccountDialog } from './Account.svelte';
  import Help, {showHelpDialog } from './Help.svelte';
  import LocationSelector from './LocationSelector.svelte';
  import { showSearchHelpDialog } from './SearchHelp.svelte';
  import { showSubscribeDialog } from './Subscribe.svelte';
  import Modal, {showModalDialog } from './Modal.svelte';
  import { fade, slide } from 'svelte/transition';
  import Select, {Option} from '@smui/select';
  import {subscriptionNew } from './binoas.js';

  let prominent = false;
  let dense = false;
  let secondaryColor = true; // false;
  let selectedLocations;
  let newQuery = "windmolens";
  let oldQuery = newQuery;
  let oldSelectedLocations = selectedLocations;
  let email;
  let typeTimer = null;
  let showAdvancedOptions = false;
  let advancedChevron = "expand_more";
  let frequency = "24h";
  let group = 1;
  let checkedSources = $sources.map(function (s) { return s.short;});
  let description = '';

  // $: newQuery = $selected_inquiry.length > 0 ? $selected_inquiry[0].user_query : '';
  $: if (selectedLocations != oldSelectedLocations) { handleQueryChange() }
  $: if ($identity) { email=$identity.email }
  $: if ($selected_inquiry_id) {description = $selected_inquiry[0].name }


  function handleSubscription() {
    var selectedLocationIds = selectedLocations.map((l) => l.value).filter((l) => l != "*");
    var selectedSources = checkedSources;
    if (checkedSources.length == $sources.length) {
      selectedSources = [];
    }
    console.log('subscription selected locations:', selectedLocationIds);
    console.log('subscription selected sources', selectedSources);
    subscriptionNew(newQuery, selectedLocationIds, selectedSources, description, email, frequency);
    showModalDialog();
  }

  function handleWithTypeTimer() {
      if (typeof(typeTimer) !== 'object') {
        clearTimeout(typeTimer);
        typeTimer = null;
      }
      typeTimer = setTimeout(function () {
        handleQueryChange();
        typeTimer = null;
      }, 200);
  }

  function toggleAdvancedOptions() {
    console.log('advanced options!');
    showAdvancedOptions = !showAdvancedOptions;
    if (showAdvancedOptions) {
      advancedChevron = "expand_less";
    } else {
      advancedChevron = "expand_more";
    }
  }

  function doAddInquiry() {
    if (typeof(selectedLocations) == 'undefined') {
      selectedLocations = [{'value': '*', 'label': 'Alle gemeenten'}];
    } else {
      if (selectedLocations.length > 1) {
        selectedLocations = selectedLocations.filter(function (l) { return (l.value != '*');})
      }
    }
    console.dir('selected locations:', selectedLocations);
    var selected_ids = selectedLocations.map(function (l) { return l.value; });
    var selected_names = selectedLocations.map(function (l) { return l.label; })
    var selected = $locations.filter(l => selected_ids.indexOf(l.id) >= 0);
    name = selected_names.join(", ");
    if (name == '*') {
      name = 'Alle gemeenten';
    }
    if (newQuery == '') {
      newQuery = "*"
    }
    if (name.indexOf(' ' + newQuery) < 0) {
      name = name + ' ' + newQuery;
    }
    console.log('adding name:' + name);
    console.log('adding selected : ');
    console.dir(selected);

    var oldColumnId = $selected_inquiry_id;
    // TODO: maybe we should do this async?
    var col_def = {
      name: name,
      locations: selected_ids,
      user_query: newQuery
    };
    console.log('checked : ', checkedSources);
    $sources.forEach(function (s) {
      col_def['src_' + s.short] = (checkedSources.indexOf(s.short) >= 0);
    });
    console.log('checked col def:', col_def);
    addInquiry(col_def);

    removeInquiry(oldColumnId);
  }

  function handleQueryChange(e){
      console.log('new query change should be handled!:');
      doAddInquiry();
      oldQuery = newQuery;
      oldSelectedLocations = selectedLocations;
  }

  $: if ($fetchingEnabled && ($inquiries.length <= 0)) { doAddInquiry()}
</script>

<style>
  .sub-toolbar {
    margin: 30px auto 30px auto;
    width: 100%;
    border-radius: 5px;
    background: #FFF;
    box-shadow: 0px 0px 8px 0px rgba(0, 0, 0, 0.15);
  }
  .flexy {
     display: flex;
     flex-flow: row wrap;
     align-items: start;
     justify-content: space-around;
  }
  .flexy-start {
    justify-content: flex-start !important;
  }
  .flexy-alt {
    background: #F9F9FA;
    justify-content: flex-end;
  }
  .flexy-alt2 {
    padding-bottom: 30px;
  }
  /*
  .sub-toolbar>div {
    margin: 30px;
  }*/
  .margined input {
    margin: 0 10px;
  }
  .bordered {
    border: 1px solid black;
    border-radius: 5px;
    background: white;
  }
  .cell-auto-flex {
    flex: 1 auto;
  }
  .cell {
      min-height: 56px;
      margin: 30px 15px;
      align-items: center;
      display: flex;
  }

  .checkbox-source {
    margin-left: 15px;
  }

  @media (max-width: 890px) {
    .cell {
      margin: 10px 5px;
    }
    .sub-toolbar {
      margin: 10px auto 10px auto;
    }
    .flexy-alt2 {
      padding-bottom: 10px;
    }
  }
  @media (min-width: 675px) {

  .cell-col {
    flex-direction: column;
  }

  .cell select {
    margin-top: 4px;
  }
}
</style>
