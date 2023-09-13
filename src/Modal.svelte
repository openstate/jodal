<Dialog
  bind:open
  bind:this={modalDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title"><slot name="modalTitle">Melding</slot></Title>
  <Content id="default-focus-content">
  <slot name="modalContent">Inhoud</slot>
  </Content>
  <Actions>
    <Button
      default
      use={[InitialFocus]}
      on:click={() => (response = 'It will be glorious.')}
    >
      <Label><slot name="modalAction">Sluiten</slot></Label>
    </Button>
  </Actions>
</Dialog>

<script>
  import Dialog, { Title, Content, Actions, InitialFocus } from '@smui/dialog';
  import Button, { Label } from '@smui/button';

  let open;
  let response = 'Nothing yet.';
</script>

<script context="module">
  let modalDialog;

	export function showModalDialog() {
    modalDialog.open();
	}
</script>
