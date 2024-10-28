<p>{message}</p>

<script>
import { fetchDocument } from './stores.js';

export let id = "";

let message = "Je wordt even omgeleid, een momentje geduld..."

function loadDocument() {
  console.log('ready to load document data ' + id);
  fetchDocument(id).then(function (data) {
    console.log('got document data:', data);
    if (data.hits.total.value == 0) {
      message = 'Het document kon niet worden gevonden.';
      return;
    }

    const source = data.hits.hits[0]._source;

    // Hotfix: Open Besluitvorming URLs are broken.
    if (source.source == 'openbesluitvorming') {
      message = "Het document wordt nu gedownload."
      window.location = source.doc_url;
    } else {
      window.location = source.url;
    }
  });
}
$: if(id != "") { loadDocument() }
</script>

<style>
  p {
    margin-inline: 1rem;
  }
</style>