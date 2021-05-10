<Dialog
  id="dialog-doc"
  bind:open
  bind:this={docDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
  class="document-dialog"
>
  <Title id="default-focus-title">{$item.title}</Title>
  <Content id="default-focus-content">
    <div class="document-dialog-content-tools">
      { @html $description }
    </div>
    <div class="document-dialog-content-description">
      { @html $item.highlighted_description }
    </div>
  </Content>
  <Actions>
    <a href="{$item.url}" target="_blank" class="mdc-button">
      <Label>Ga naar bron</Label>
    </a>

    <Button
      default
      use={[InitialFocus]}
      on:click={() => (response = 'It will be glorious.')}
    >
      <Label>Sluiten</Label>
    </Button>
  </Actions>
</Dialog>

<script>
  import Dialog, { Title, Content, Actions, InitialFocus } from '@smui/dialog';
  import Button, { Label } from '@smui/button';
  import { writable, get, derived } from 'svelte/store';

  let open;
  let response = 'Nothing yet.';

</script>

<script context="module">
  let docDialog;
  let item = writable({});
  let description = writable("");

  function getDocumentTools() {
    var url = 'https://blog.jodal.nl/?page_id=14&content-only=1';
    return fetch(
      url, {cache: 'no-cache'})
        .then(res => {
            return res.text();
        }).then(
          function (data) {
            console.log('got document data:');
            console.dir(data);
            description.set(data);
          }
      );
  }

	export function showDocumentDialog(doc) {
    if (typeof(doc.highlight) !== 'undefined') {
      var highlight_tags_removed = doc.highlight.replace('<em>', '').replace('</em>', '');
      doc.highlighted_description = doc.description.replaceAll(highlight_tags_removed, doc.highlight);
    } else {
      doc.highlighted_description = doc.description;
    }
    item.set(doc);
    getDocumentTools();
    docDialog.open();
	}
</script>
