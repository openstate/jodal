<div class="sub-toolbar">
  <div class="flexy">
    <div>
      <Textfield>
        <Input bind:value={newQuery} id="column-query" aria-controls="helper-text-column-query" aria-describedby="helper-text-column-query" />
        <FloatingLabel for="input-column-name">Zoekopdracht</FloatingLabel>
        <LineRipple />
        <IconButton align="end" class="material-icons" aria-label="Hulp bij een zoekopdracht maken" alt="Hulp bij een zoekopdracht maken" on:click={() => showSearchHelpDialog()}>info</IconButton>
      </Textfield>
      <HelperText id="helper-text-column-name">De zoekopdracht</HelperText>
    </div>
    <div>
      <LocationSelector bind:selectedLocations showEmptyButton={false}/>
    </div>
    <div>
      <IconButton id="btn-icon-add-column" class="material-icons" aria-label="Add a column" title="Zoekopdracht toevoegen" on:click={() => handleQueryChange()}>add</IconButton>
    </div>
    <div>
      <Button on:click={() => showSubscribeDialog($selected_inquiry.user_query, $selected_inquiry.locations)}>Abboneer</Button>
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

  // $: newQuery = $selected_inquiry.length > 0 ? $selected_inquiry[0].user_query : '';

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
  }

  $: if ($fetchingEnabled && ($inquiries.length <= 0)) { doAddInquiry()}
</script>

<style>
  .sub-toolbar {
    margin: 0 auto;
    width: fit-content;
  }
  .flexy {
    display: flex;
    flex-wrap: wrap;
  }
</style>
