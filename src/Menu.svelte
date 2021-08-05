<section>
      <TopAppBar variant="static" {prominent} {dense} color={secondaryColor ? 'secondary' : 'primary'}>
        <Row>
          <Section>
            <IconButton class="material-icons"  on:click={() => drawerOpen.update(n => !n)}>menu</IconButton>
            <Title>Journalistiek Dashboard Lokaal - Beta</Title>
          </Section>
          <Section align="end" toolbar>
          <IconButton class="material-icons" aria-label="Login" on:click={() => showHelpDialog()} title="Om hulp vragen">help</IconButton>
          {#if $identity}
            <IconButton class="material-icons" aria-label="Add a column" title="Zoekopdracht toevoegen" on:click={() => startAddColumn()}>add</IconButton>
            <IconButton class="material-icons" aria-label="Account" title="Account informatie" on:click={() => showAccountDialog()}>face</IconButton>
            <IconButton class="material-icons" aria-label="Logout" href="//api.jodal.nl/users/simple/logout" title="Uitloggen">login</IconButton>
          {:else}
            <IconButton class="material-icons" aria-label="Login" href="//api.jodal.nl/users/simple/login" title="Inloggen">account_box</IconButton>
          {/if}
          </Section>
        </Row>
      </TopAppBar>
</section>
<Help/>
<Account/>
<AddColumn/>
<script>
  import { drawerOpen,fetchingEnabled, identity } from './stores.js';
  import AddColumn, { startAddColumn } from './AddColumn.svelte';
  import Help, { showHelpDialog } from './Help.svelte';
  import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
  import IconButton from '@smui/icon-button';
  import Checkbox from '@smui/checkbox';
  import FormField from '@smui/form-field';
  import Account, { showAccountDialog } from './Account.svelte';

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
