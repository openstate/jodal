<div class="sub-toolbar">
  <div class="flexy">
    <div class="bordered">
      <Textfield>
        <Input bind:value={newQuery} id="column-query" aria-controls="helper-text-column-query" aria-describedby="helper-text-column-query" on:change={() => handleQueryChange()} on:blur={() => handleQueryChange()} on:keyup={() => handleWithTypeTimer()} />
      </Textfield>
    </div>
    <div class="bordered">
      <LocationSelector bind:selectedLocations showEmptyButton={false}/>
    </div>
  </div>
  <div class="flexy">
    <div>
      <input bind:value={email} id="subscribe-email" />
    </div>
    <div>
      <Button on:click={() => showSubscribeDialog($selected_inquiry.user_query, $selected_inquiry.locations)}>Abboneer</Button>
    </div>
    <div>
    <a href="#">Meer opties</a>
    </div>
  </div>
</div>
<script>
  import { addInquiry, removeInquiry, inquiries, locations, selectable_locations, id2locations, drawerOpen,fetchingEnabled, identity, isTesting, apiDomainName, domainName, selected_inquiry, selected_inquiry_id } from './stores.js';
  import AddColumn, { startAddColumn } from './AddColumn.svelte';
  import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
  import IconButton from '@smui/icon-button';
  import Button from '@smui/button';
  import Checkbox from '@smui/checkbox';
  import {Label} from '@smui/fab';
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
  let prominent = false;
  let dense = false;
  let secondaryColor = true; // false;
  let selectedLocations;
  let newQuery = "windmolens";
  let oldQuery = newQuery;
  let oldSelectedLocations = selectedLocations;
  let email;
  let typeTimer = null;

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
    margin: 0 auto;
    width: 100%;
    border-radius: 5px;
    background: #FFF;
    box-shadow: 0px 0px 8px 0px rgba(0, 0, 0, 0.15);
  }
  .flexy {
    display: flex;
    flex-wrap: wrap;
    align-items: start;
  }
  .sub-toolbar>div {
    margin: 30px;
  }
  .sub-toolbar .bordered {
      margin: 10px;
      height: 56px;
      border: 1px solid black;
      border-radius: 5px;
      max-width: 50%;
  }
</style>
