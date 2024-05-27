<Dialog
  bind:open
  bind:this={loginDialogObj}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">Inloggen</Title>
  <Content id="default-focus-content">
  <Label class="input-label">E-mail adres</Label>
  <input  class="input-full-width input-full-height" bind:value={emailAddress} id="forgot-email" />
  </Content>
  <Actions>
    <Button
      default
      use={[InitialFocus]}
      on:click={(e) => (startPasswordlessLogin(e))}
    >
      <Label>Inloggen</Label>
    </Button>
  </Actions>
</Dialog>

<script>
  import Dialog, { Title, Content, Actions, InitialFocus } from '@smui/dialog';
  import Button, { Label } from '@smui/button';

  import { apiDomainName, loginDialogOpen } from './stores.js';

  let open;
  let response = '';
  let emailAddress = "";

  function startPasswordlessLogin(e) {
    //e.preventDefault();
    var url = window.location.protocol + '//' + apiDomainName + '/users/passwordless/start?email=' + encodeURIComponent(emailAddress);
    return fetch(
      url, {cache: 'no-cache'}).then(
        response => response.json()
      ).then(
        function (data) {
          console.log('login passwordless start response:', data);
          response = 'Er is zojuis een e-mail gestuurd met verdere instructies om in te loggen.'
          $loginDialogOpen = false;
        }
      );
  }
</script>

<script context="module">
  let loginDialogObj;

	export function showLoginDialog() {
    loginDialogObj.open();
	}
</script>

<style>
.input-full-height {
  height: 54px;
}

.input-full-width {
  width: 80% !important;
}

input {
	border: 1px solid black;
	border-radius: 5px;
	line-height: 32px;
  padding: 0 20px;
  margin: 10px 0 10px 0;
}
</style>
