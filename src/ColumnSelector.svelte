<div class="column-selector">
  <ul>
  {#each $ordered_inquiries as inq}
    <li data-id="{inq.id}" data-query="{inq.user_query}">{inq.name}</li>
  {/each}
  </ul>
</div>

<script>
import { ordered_inquiries, inquiries, identity, isTesting, apiDomainName, domainName, selected_inquiry_id, selected_inquiry } from './stores.js';

let empty = ($inquiries.length <= 0);
</script>

<style>
</style>
