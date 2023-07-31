<div class="sub-toolbar flexy">
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
<script>
  import { drawerOpen,fetchingEnabled, identity, isTesting, apiDomainName, domainName } from './stores.js';
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

  function handleQueryChange(e){
      console.log('new query change should be handled!:');
  }
</script>

<style>
  .top-app-bar-container, .top-app-bar-iframe {
    max-width: 480px;
    min-width: 480px;
    height: 320px;
    border: 1px solid rgba(0,0,0,.1);
    margin: 0 18px 18px 0;
  }

  .top-app-bar-container {
    overflow: auto;
    display: inline-block;
  }

  .flexy {
    display: flex;
    flex-wrap: wrap;
  }

  .flexor {
    display: inline-flex;
    flex-direction: column;
  }

  .flexor-content {
    flex-basis: 0;
    height: 0;
    flex-grow: 1;
    overflow: auto;
  }
</style>
