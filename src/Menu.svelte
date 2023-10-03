<header>
  <div class="menu-hamburger menu-part">
    <IconButton class="material-icons"  on:click={() => drawerOpen.update(n => !n)}>menu</IconButton>
  </div>
  <div class="logo-container menu-part">
    <a href="/"><img src="/images/bron-logo.svg" alt="Bron logo" /></a>
  </div>
  <div class="menu-part logo-description-container">
    <p class="logo-description"><span>alle overheidsdata</span><span> — </span><span>monitor, filter, stuur door.</span></p>
  </div>
  <div class="menu-container menu-part">
    <Link class="menu-link" to="bronnen">Bronnen</Link>
    <Link class="menu-link" to="over">Over Ons</Link>
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
  import { Link } from "svelte-routing";
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
.logo-container img {
  width: 190px;
  height: 40px;
}

.logo-description {
  font-size: 17px;
  line-height:48px;
  font-weight: 400;
  color: #767676;
  margin-left: 30px;
  text-align: left;
}

.logo-description san {
  display: inline;
}

@media (max-width: 950px) {
	.menu-container {
		display: none !important;
	}

}

@media (min-width: 1025px) {
  .logo-description-container {
    flex: 1;
  }
}

@media (min-width: 950px) {
	.menu-hamburger {
		display: none !important;
	}

  .logo-container {
    margin-left: 10px;
  }

}

@media (max-width: 676px) {
  .logo-container {
    margin-top: 10px;
    margin-right: 10px;
  }
}
@media (max-width: 556px) {
  .logo-description {
    text-align: center;
  }
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

@media (max-width: 412px) {
    .logo-description span {
      display: inline-block;
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

</style>
