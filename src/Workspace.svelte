<div class="workspace" id="workspace">
  <div class="columns">
  <div class="workspace-header">
    <h1>Alerts</h1>
    <p>Scan alle nieuwe overheidsdocumenten en ontvang de belangrijkste in je e-mail.</p>
  </div>
  <AddColumnBar/>
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
.workspace-header {
  text-align: center;
}

.workspace-header p {
  color: #5E5E5E;
}
</style>
