<svelte:head>
  <title>Jodal</title>
</svelte:head>

<section>
      <TopAppBar variant="static" {prominent} {dense} color={secondaryColor ? 'secondary' : 'primary'}>
        <Row>
          <Section>
            <IconButton class="material-icons"  on:click={() => drawerOpen.update(n => !n)}>menu</IconButton>
            <Title>Jodal</Title>
          </Section>
          <Section align="end" toolbar>
            <IconButton class="material-icons" aria-label="Add a column" on:click={() => startAddColumn()}>add</IconButton>
          </Section>
        </Row>
      </TopAppBar>
</section>

<AddColumn/>
<script>
  import { drawerOpen } from './stores.js';
  import AddColumn, { startAddColumn } from './AddColumn.svelte';
  import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
  import IconButton from '@smui/icon-button';
  import Checkbox from '@smui/checkbox';
  import FormField from '@smui/form-field';

  let prominent = false;
  let dense = false;
  let secondaryColor = false;
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
