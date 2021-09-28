<Dialog
  bind:open
  bind:this={accountDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">Account</Title>
  <Content id="default-focus-content">
    <p><strong>Email:</strong> {$identity.email}</p>
    <Button
      variant="unelevated"
      on:click={function () {
          if (confirm('Weet je zeker dat je je account wilt verwijderen? Dit kan niet meer ongedaan maken.')) {
            window.location = window.location.protocol + '//api.jodal.nl/users/delete';
          }
      }}
    >
      <Label>Account verwijderen</Label>
    </Button>
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
  import { identity } from './stores.js';

  let open;
  let response = 'Nothing yet.';
</script>

<script context="module">
  let accountDialog;

	export function showAccountDialog() {
    accountDialog.open();
	}
</script>
