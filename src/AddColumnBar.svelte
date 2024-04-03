<Modal>
  <div slot="modalTitle">Melding</div>
  <div slot="modalContent">{modalMsg}</div>
</Modal>
<form>
<div class="sub-toolbar">
  <div class="flexy">
    <div class="cell cell-auto-flex">
      <Label class="input-label">Zoekopdracht</Label>
      <div class="flexy no-gap">
        <input  class="input-full-width input-full-height" bind:value={newQuery} id="column-query" aria-controls="helper-text-column-query" aria-describedby="helper-text-column-query" on:change={() => handleQueryChange()} on:focus={() => isEditFieldActive = true } on:blur={() => handleQueryChange()} on:keyup={() => handleWithTypeTimer()} />
        <p class="input-help">Bijvoorbeeld: windmolens | parken  | windenergie | subsidie</p>
      </div>
    </div>
  </div>
  <div class="flexy">
    <div class="cell cell-auto-flex">
      <Label class="input-label">Zoekgebied</Label>
      <LocationSelector bind:selectedLocations showEmptyButton={false}/>
      <p class="input-help">Selecteer gemeenten, provincies of ministeries waarin je wilt zoeken.</p>
    </div>
  </div>
  <div class="flexy flexy-start">
    <div class="cell flexy-min">
      <a href="#" on:click={() => toggleAdvancedOptions()}>Meer opties</a>
      <Icon class="material-icons expand-more">{advancedChevron}</Icon>
    </div>
  </div>
  {#if showAdvancedOptions}
  <div class="flexy flexy-start flexy-alt flexy-alt2 no-bottom-margin"  transition:slide="{{ duration: 500 }}">
    <div class="cell cell-col">
    <h4 class="no-margin">Bronnen</h4>
    <div class="flexy flexy-start">
    {#each $sources as s}
      <div class="checkbox-source">
      <input type="checkbox" id="source-checkbox-{s.short}" class="input-checkbox" name="source"  bind:group={checkedSources} value="{s.short}" on:change={() => handleQueryChange()}><label for="source-checkbox-{s.short}">{s.name}</label>
      </div>
    {/each}
    </div>
    </div>
  </div>
  {/if}
  <div class="flexy flexy-alt flexy-submit">
    <div class="cell cell-auto-flex flexy">
      <input class="input-full-height input-full-width no-margin" bind:value={email} id="subscribe-email" type="email" placeholder="E-mail" required />
    </div>
    <div class="cell cell-auto-flex flexy">
      <select class="input-frequency input-full-width" bind:value={frequency}>
        <option value="" selected={frequency == ''}>Direct</option>
        <option value="1h" selected={frequency == '1h'}>Elk uur</option>
        <option value="24h" selected={frequency == '24h'}>Elke dag</option>
        <option value="168h" selected={frequency == '168h'}>Elke week</option>
      </select>
    </div>
    <div class="cell cell-auto-flex flexy">
      <a href="#" id="rss-button mdc-button" class="subscribe-button mdc-button">RSS</a>
    </div>
    <div class="cell cell-auto-flex flexy">
      <Button class="subscribe-button input-full-width" style="width: 100%" on:click={(e) => handleSubscription(e)}>Maak alert aan</Button>
      <p class="input-help">Afmelden kan met &eacute;&eacute;n klik.</p>
    </div>
  </div>
</div>
</form>
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
  let defaultModalMsg = 'Het aanmelden is gelukt. Je krijgt ook een mailtje hierover in je mailbox.';
  let modalMsg = defaultModalMsg;
  let isEditFieldActive = false;

  // $: newQuery = $selected_inquiry.length > 0 ? $selected_inquiry[0].user_query : '';
  $: if (selectedLocations != oldSelectedLocations) { handleQueryChange() }
  $: if ($identity) { email=$identity.email }
  $: if ($selected_inquiry_id) {description = $selected_inquiry[0].name }


  function handleSubscription(e) {
    console.log('subscription event: ', e);
    e.preventDefault();
    var selectedLocationIds = selectedLocations.map((l) => l.value).filter((l) => l != "*");
    var selectedSources = checkedSources;
    if (checkedSources.length == $sources.length) {
      selectedSources = [];
    }
    console.log('subscription selected locations:', selectedLocationIds);
    console.log('subscription selected sources', selectedSources);
    const emailRegex = new RegExp(/^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9.-]+$/, "gm");
    const isValidEmail = emailRegex.test(email);
    console.log('Valid email: ' + email, isValidEmail);
    if (document.getElementById('subscribe-email').validity.valid && isValidEmail) {
      subscriptionNew(newQuery, selectedLocationIds, selectedSources, description, email, frequency).then(
      function (data) {
        console.log(data);
        if (typeof(data.error) !== 'undefined') {
          modalMsg = 'Er ging iets mis met het aanmaken van de alert. Probeer het later nog een keer.'
        } else {
          modalMsg = defaultModalMsg;
        }
        showModalDialog();
      });
    } else {
      if (e.explicitOriginalTarget.id != 'column-query') {
        modalMsg = 'Er is geen valide e-mail adres ingevuld. Probeer het opnieuw.';
        showModalDialog();
      }
    }
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
      selectedLocations = [{'value': '*', 'label': 'Alles'}];
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
      name = 'Alles';
    }
    // if (newQuery == '') {
    //   newQuery = "*"
    // }
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
.input-full-height {
  height: 54px;
}

.input-full-width {
  width: 100% !important;
}

.input-frequency {
  font-size: 16px;
  line-height: 32px;
  height: 56px;
  margin: 0;
  padding: 0 20px;
  background: white;
  border: 1px solid black;
  border-radius: 5px;
  appearance: none;
}

.input-help {
  font-size: 12px;
  font-weight: 500;
  text-align: right;
  width: 100%;
  margin: 0;
  color: #5E5E5E;
}
input {
	border: 1px solid black;
	border-radius: 5px;
	line-height: 32px;
  padding: 0 20px;
  margin: 10px 0 10px 0;
}
.input-checkbox {
  margin-right: 10px;
}
.no-bottom-margin {
  margin-bottom: 0 !important;
}
.no-margin {
  margin: 0 !important
}
.no-gap {
  gap: 0 !important;
}
  .sub-toolbar {
    padding: 30px 30px;
    margin: 30px auto 65px auto;
    /*width: 100%;*/
    border-radius: 5px;
    background: #F9F9FA;
    line-height: 16px;
  }

  .flexy-min {
      display: flex;
  }

  .flexy {
     display: flex;
     flex-flow: row wrap;
     gap: 0 20px;
     align-items: start;
     justify-content: space-around;
     background: #F9F9FA;
     margin-bottom: 20px;
  }

.flexy:last-child {
  margin-bottom: 0px !important;
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
    min-height: 39px;
  }
  .flexy-alt .cell {
    min-height: 39px !important;
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
      /*margin: 5px 30px;*/
      align-items: center;
  /*    display: flex;*/
/*
  flex: 1 auto;
*/
  }

  .checkbox-source {
    margin-right: 15px;
  }

.cell-noright {
  margin-right: 0 !important;
}

@media (max-width: 440px) {
  .sub-toolbar {
    padding: 30px 20px !important;
  }
}

  @media (max-width: 890px) {
    .cell {
      margin: 5px 5px;
    }
    .sub-toolbar {
      margin: 10px auto 10px auto;
      padding: 20px;
    }
    .flexy-alt2 {
      padding-bottom: 10px;
    }
  }
  @media (min-width: 675px) {

  .cell-col {
    flex-direction: column;
  }

.cell-col h4 {
  margin: 0 !important;
}
  .cell select {
    margin-top: 0px;
  }

}
</style>
