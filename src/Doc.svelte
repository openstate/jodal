<h1>Doc {id}</h1>

<script>
import { fetchDocument } from './stores.js';
import { showDocumentDialog } from './Document.svelte';
export let id = "";

function loadDocument() {
  console.log('ready to load document data ' + id);
  fetchDocument(id).then(function (data) {
    console.log('got document data:', data);
    if (data.hits.total.value > 0) {
      showDocumentDialog(data.hits.hits[0]._source);
    }
  });
}
$: if(id != "") { loadDocument() }
</script>
