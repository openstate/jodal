<Dialog
  bind:open
  bind:this={helpDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">Help</Title>
  <Content id="default-focus-content">
    Als je vragen hebt kan je ons altijd mailen op <a href="mailto:jodal@openstate.eu?Subject=Help">jodal@openstate.eu</a>. Er is ook een <a href="//www.jodal.nl/privacy/" target="_blank">privacy statement</a>.
  </Content>
  <Actions>
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

  let open;
  let response = 'Nothing yet.';
</script>

<script context="module">
  let helpDialog;

	export function showHelpDialog() {
    helpDialog.open();
	}
</script>
