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
      <IconButton id="btn-icon-add-column" class="material-icons" aria-label="Add a column" title="Zoekopdracht toevoegen" on:click={() => startAddColumn()}>add</IconButton>
    </div>
  </div>
</div>
<script>
  import { drawerOpen,fetchingEnabled, identity, isTesting, apiDomainName, domainName, selected_inquiry, selected_inquiry_id } from './stores.js';
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

  let prominent = false;
  let dense = false;
  let secondaryColor = true; // false;
  let selectedLocations;
  let newQuery;

  // $: newQuery = $selected_inquiry.length > 0 ? $selected_inquiry[0].user_query : '';

  function handleQueryChange(e){
      console.log('new query change should be handled!:');
  }
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
