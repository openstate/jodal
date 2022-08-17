<div class="workspace" id="workspace">
  <div class="columns">
  {#if $isTesting}
    <div class="message message-warning">
      <span>Hier kun je Jodal uitproberen! De zoekopdrachten zullen niet worden opgeslagen.</span>
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
    	<Column inquiry={inq} />
    {/each}
  {:else}
  <div class="start-explainer">
    <p>Je bent niet ingelogd. Klik op de &eacute;&eacute;n van de knoppen hieronder om in te loggen of een account aan te maken.</p>
    <Button align="end" href="//www.jodal.nl/login/"><Label>Inloggen</Label></Button> of
    <Button align="end" href="//api.jodal.nl//www.jodal.nl/register/"><Label>Registreren</Label></Button>
  </div>
  {/if}
  </div>
</div>

<script>
import { ordered_inquiries, inquiries, identity, isTesting } from './stores.js';
import Column from './column/Column.svelte';
import AddColumn, { startAddColumn } from './AddColumn.svelte';
import Button from '@smui/button';
import Fab, {Label, Icon} from '@smui/fab';
import Message from './Message.svelte';
import Interview from './Interview.svelte';

let empty = ($inquiries.length <= 0);
</script>

<style>
</style>
