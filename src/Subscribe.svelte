<Dialog
  bind:open
  bind:this={subscribeDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">Abboneer</Title>
  <Content id="default-focus-content">
    input email hiero
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
  let subscribeDialog;

	export function showSubscribeDialog() {
    subscribeDialog.open();
	}
</script>
