<div class="workspace" id="workspace">
  <div class="columns">
  <AddColumnBar/>
  {#if $isTesting}
    <div class="message message-warning">
      <span>Hier kun je Open Overheidsdata uitproberen! De zoekopdrachten zullen niet worden opgeslagen.</span>
    </div>
  {/if}
  {#if $identity || $isTesting}
    <Message/>
    {#if $isTesting}
      <Interview/>
    {/if}
    {#if $inquiries.length <= 0}
    <section class="column-section">
    <div id="column-contents-new-inq" class="column-contents">
      <p>Je hebt nog geen zoekopdracht toegevoegd. Klik op de knop hieronder om er een toe te voegen.</p>
      <Button align="end" on:click={() => startAddColumn()}><Label>Zoekopdracht toevoegen</Label></Button>
    </div>
    </section>
    {/if}
    {#each $ordered_inquiries as inq}
      {#if inq.id == $selected_inquiry_id}
    	<Column inquiry={inq} />
      {/if}
    {/each}
  {:else}
  <div class="start-explainer">
    <p>Je bent niet ingelogd. Klik op de &eacute;&eacute;n van de knoppen hieronder om in te loggen of een account aan te maken.</p>
    <Button align="end" href="//www.{domainName}/login/"><Label>Inloggen</Label></Button> of
    <Button align="end" href="//www.{domainName}/register/"><Label>Registreren</Label></Button>
  </div>
  {/if}
  </div>
</div>

<script>
import { ordered_inquiries, inquiries, identity, isTesting, apiDomainName, domainName, selected_inquiry_id, selected_inquiry } from './stores.js';
import Column from './column/Column.svelte';
import AddColumn, { startAddColumn } from './AddColumn.svelte';
import Button from '@smui/button';
import Fab, {Label, Icon} from '@smui/fab';
import Message from './Message.svelte';
import Interview from './Interview.svelte';
import AddColumnBar from './AddColumnBar.svelte';

let empty = ($inquiries.length <= 0);
</script>

<style>
</style>
