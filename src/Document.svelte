<Dialog
  id="dialog-doc"
  bind:open
  bind:this={docDialog}
  on:MDCDialog:opened={() => scrollHighlightIntoView()}
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
    {#if $item.source == 'openspending' && (typeof($item.data) !== 'undefined') && (typeof($item.data.label) !== 'undefined')}
    <Group style="margin-right: 4em;">
      <Label style="margin: 2px; line-height: 28px; margin-right: 1em;">Downloaden als:</Label>
      {#each export_formats[$item.source] as fmt}
        <a href="//api.jodal.nl/documents/download/{$item.source}/{$item.data.label.document_id}?format={fmt}" target="_blank" class="mdc-button">
          <Label>{fmt}</Label>
        </a>
      {/each}
    </Group>
    {/if}

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
  import Button, { Group, GroupItem, Label, Icon } from '@smui/button';
  import { writable, get, derived } from 'svelte/store';

  let open;
  let response = 'Nothing yet.';
  let export_formats = {
    'openspending': ['csv', 'json']
  };
  function scrollHighlightIntoView() {
    var highlight_em = document.getElementsByClassName('document-dialog-content-description')[0].getElementsByTagName('em');
    console.log(highlight_em);
    if (highlight_em.length > 0) {
      console.log('SCROLL INTO VIEW');
      highlight_em[0].scrollIntoView();
      highlight_em[0].scrollBy(0, -60); // small correction bc somethings thing is not shown
    }
  }
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
      if (typeof(doc.description) !== 'undefined') {
        doc.highlighted_description = doc.description.replaceAll(highlight_tags_removed, doc.highlight);
      } else {
        doc.highlighted_description = doc.highlight;
      }
    } else {
      doc.highlighted_description = doc.description;
    }
    item.set(doc);
    getDocumentTools();
    docDialog.open();
	}
</script>
