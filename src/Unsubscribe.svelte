<Modal>
  <div slot="modalTitle">Alert stopzetten</div>
  <div slot="modalContent">{modalMsg}</div>
</Modal>

<script>
import { addInquiry, removeInquiry, inquiries, locations, selectable_locations, id2locations, sources, drawerOpen,fetchingEnabled, identity, isTesting, apiDomainName, domainName, selected_inquiry, selected_inquiry_id } from './stores.js';
import Modal, {showModalDialog } from './Modal.svelte';
import { subscriptionDelete } from './binoas.js';

export let user_id = "";
export let query_id = "";
let defaultModalMsg = "De alert is stopgezet.";
let modalMsg = defaultModalMsg;

function unsubscribe() {

  subscriptionDelete(user_id, query_id).then(
  function (data) {
    console.log(data);
    if (typeof(data.error) !== 'undefined') {
      modalMsg = 'Er ging iets mis met het stopzetten van de alert. Probeer het later nog een keer.'
    } else {
      modalMsg = defaultModalMsg;
    }
    showModalDialog();
  });

}

$: if(user_id != "") { unsubscribe() }

</script>
