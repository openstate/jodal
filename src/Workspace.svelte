<div class="workspace" id="workspace">
  <div class="columns">
  <div class="workspace-header">

    <h1><img src="/images/alert.svg" style="width: 25px;" /> Alerts</h1>
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
  margin-top: 90px;
  text-align: center;
}

@media (min-width: 950px) {
  .hide-smallscreen {
    display: inline-flex !important;
  }
  .show-smallscreen{
    display: none !important;
  }
}

@media (max-width: 950px) {
  .hide-smallscreen {
    display: none !important;
  }
  .show-smallscreen{
    display: inline-flex !important;
  }

	.workspace-header {
		margin-top: 60px;
		overflow: hidden;
		text-overflow: ellipsis;
	}
}

@media (max-width: 438px) {
	.workspace-header {
		margin-top: 30px;
		overflow: hidden;
		text-overflow: ellipsis;
	}
}

.workspace-header p {
  color: #5E5E5E;
  text-align: center;
  font-size: 18px;
}

@media (max-width: 438px) {
  .workspace-header p {
    color: #5E5E5E;
    text-align: center;
    font-size: 16px;
    line-height: 25px;
    padding: 0px 20px 20px;
  }

  .workspace-header {
    margin-top: 20px;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}
</style>
