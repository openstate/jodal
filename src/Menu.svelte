<header>
  <div class="logo-container menu-part">
    <h1>De bron</h1>
    <p class="logo-description">alle overheidsdata — monitor, filter, stuur door.</p>
  </div>
  <div class="menu-container menu-part">
    <a href="#p/bronnen">Bronnen</a>
    <a href="#p/over-ons">Over Ons</a>
    <IconButton id="btn-icon-help" class="material-icons" aria-label="Hulp" title="Om hulp vragen" on:click={() => showHelpDialog()}>help</IconButton>
    {#if $identity}
      <IconButton id="btn-icon-add-column" class="material-icons" aria-label="Add a column" title="Zoekopdracht toevoegen" on:click={() => startAddColumn()}>add</IconButton>
      <IconButton id="btn-icon-account" class="material-icons" aria-label="Account" title="Account informatie" on:click={() => showAccountDialog()}>face</IconButton>
      <IconButton id="btn-icon-logout" class="material-icons" aria-label="Logout" href="//{apiDomainName}/users/simple/logout" title="Uitloggen">login</IconButton>
    {:else}
      <IconButton id="btn-icon-login" class="material-icons" aria-label="Login" href="//www.{domainName}/login/" title="Inloggen">account_box</IconButton>
    {/if}
  </div>
</header>
<Account/>
<AddColumn/>
<Help/>
<script>
  import { drawerOpen,fetchingEnabled, identity, isTesting, apiDomainName, domainName } from './stores.js';
  import AddColumn, { startAddColumn } from './AddColumn.svelte';
  import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
  import IconButton from '@smui/icon-button';
  import Button from '@smui/button';
  import Checkbox from '@smui/checkbox';
  import {Label} from '@smui/fab';
  import FormField from '@smui/form-field';
  import Account, { showAccountDialog } from './Account.svelte';
  import Help, {showHelpDialog } from './Help.svelte';

  $: testEnv = $isTesting ? 'Test' : 'Beta';

  let prominent = false;
  let dense = false;
  let secondaryColor = false;
  var iconName = "pause";

  function doPause() {
    console.log('FIXME: disabling fetching for now!!!!!');
    fetchingEnabled.set(!$fetchingEnabled);
    if ($fetchingEnabled) {
      iconName = "pause";
    } else {
      iconName = "play_arrow";
    }
  }
</script>

<style>
.logo-description {
  font-size: 17px;
  line-height:48px;
  font-weight: 400;
  color: #767676;
  margin-left: 30px;
}

@media (max-width: 438px) {
	.logo-description {
    font-size: 16px;
    line-height: 20px;
		overflow: hidden;
		text-overflow: ellipsis;
	}

  .menu-container a {
    font-size: 16px !important;
    line-height: 20px !important;
    margin: 0 15px !important;
  }
}

  .flexy {
    display: flex;
    flex-wrap: wrap;
  }

  .menu-part {
  	display: flex;
  	flex-flow: row wrap;
  	justify-content: space-between;
  	align-items: center;
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

  .menu-container a {
    color: #A3A3A3;
    font-size: 20px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
    margin: 30px;
    text-decoration: none;
  }
</style>
