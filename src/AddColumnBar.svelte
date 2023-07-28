<section>
      <TopAppBar variant="static" {prominent} {dense} color={secondaryColor ? 'secondary' : 'primary'}>
        <Row>
          <Section>
            <Title>Toevoegen</Title>
          </Section>
          <Section align="end" toolbar>
          <LocationSelector bind:selectedLocations />
          <IconButton id="btn-icon-add-column" class="material-icons" aria-label="Add a column" title="Zoekopdracht toevoegen" on:click={() => startAddColumn()}>add</IconButton>
          </Section>
        </Row>
      </TopAppBar>
</section>
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
  import LocationSelector from './LocationSelector.svelte';

  let prominent = false;
  let dense = false;
  let secondaryColor = false;
  let selectedLocations;

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
