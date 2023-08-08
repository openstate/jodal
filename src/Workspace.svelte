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
    {#each $ordered_inquiries as inq}
      {#if inq.id == $selected_inquiry_id}
    	<Column inquiry={inq} />
      {/if}
    {/each}
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
