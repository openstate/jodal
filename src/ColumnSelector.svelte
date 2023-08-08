<div class="column-selector">
  <ul>
  {#each $ordered_inquiries as inq}
    <li data-id="{inq.id}" data-query="{inq.user_query}" on:click={(e) => selectColumn(e)}>{inq.name}</li>
  {/each}
  </ul>
</div>

<script>
import { ordered_inquiries, inquiries, identity, isTesting, apiDomainName, domainName, selected_inquiry_id, selected_inquiry } from './stores.js';

let empty = ($inquiries.length <= 0);

function selectColumn(elem) {
  console.log('selected different column', elem);
  var new_column_id = elem.target.attributes['data-id'].nodeValue;
  console.log('selected column id:', new_column_id);
  selected_inquiry_id.set(new_column_id);
}
</script>

<style>
</style>
