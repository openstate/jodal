<Dialog
  bind:open
  bind:this={docDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">{$item.title}</Title>
  <Content id="default-focus-content">
    {$item}
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
	export function showDocumentDialog(doc) {
    item.set(doc)
    docDialog.open();
	}
</script>
