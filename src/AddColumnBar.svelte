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
      <Button class="subscribe-button" on:click={() => showSubscribeDialog($selected_inquiry.user_query, $selected_inquiry.locations)}>Maak alert aan</Button>
    </div>
    <div class="cell">
    <a href="#" on:click={() => toggleAdvancedOptions()}>Meer opties
    </a>
    <Icon class="material-icons expand-more">{advancedChevron}</Icon>
    </div>
  </div>
  {#if showAdvancedOptions}
  <div class="flexy flexy-alt"  transition:slide="{{ duration: 500 }}">
    <div class="cell">
    bronnen
    </div>
    <div class="cell">
      <select bind:value={frequency}>
        <option value="" selected={frequency == ''}>Onmiddelijk</option>
        <option value="hourly" selected={frequency == '1h'}>Elk uur</option>
        <option value="daily" selected={frequency == '24h'}>Elke dag</option>
        <option value="weekly" selected={frequency == '168h'}>Elke week</option>
      </select>
    </div>
  </div>
  {/if}
</div>
<script>
  import { addInquiry, removeInquiry, inquiries, locations, selectable_locations, id2locations, drawerOpen,fetchingEnabled, identity, isTesting, apiDomainName, domainName, selected_inquiry, selected_inquiry_id } from './stores.js';
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
  import { fade, slide } from 'svelte/transition';
  import Select, {Option} from '@smui/select';

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
  let frequency = "";
  // $: newQuery = $selected_inquiry.length > 0 ? $selected_inquiry[0].user_query : '';
  $: if (selectedLocations != oldSelectedLocations) { handleQueryChange() }


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
      alert('Selecteer 1 of meerdere lokaties om een zoekopdracht aan te maken');
      return;
    }
    console.dir('selected locations:');
    console.log(selectedLocations);
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
    addInquiry({
      name: name,
      locations: selected_ids,
      user_query: newQuery
    });

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
     padding: 30px;
  }
  .flexy-alt {
    background: #F9F9FA;
    justify-content: flex-end;
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
      height: 56px;
      margin: 0 15px;
      align-items: center;
      display: flex;
  }
</style>
