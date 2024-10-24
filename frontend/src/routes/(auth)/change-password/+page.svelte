<script lang="ts">
  import { run } from 'svelte/legacy';

  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  let errorMessage: false | string = $state(false);

  let id = $derived($page.url.searchParams.get('id'));

  run(() => {
    if (!id)
      errorMessage = 'Je kan niet je wachtwoord veranderen zonder geldige code.';
  });

  async function submit(e: SubmitEvent) {
    e.preventDefault();
    const node = e.target as HTMLFormElement;

    const response = await fetch(node.action, {
      method: node.method,
      body: new FormData(node),
      cache: 'no-cache',
    });

    const json = await response.json();

    if ('error' in json) {
      errorMessage = json.error;
      return;
    } else {
      errorMessage = false;
      goto('/login');
    }

    console.log(json);
  }
</script>

<h1>Wachtwoord veranderen</h1>

{#if errorMessage}
  <div class="alert alert-danger" role="alert">
    {errorMessage}
  </div>
{/if}

<form
  method="POST"
  action="//api.bron.live/users/change-password"
  onsubmit={submit}
>
  <input type="hidden" name="changePasswordId" value={id} />
  <input type="password" name="password" placeholder="Nieuw wachtwoord" />
  <input
    type="password"
    name="password_repeat"
    placeholder="Herhaal nieuw wachtwoord"
  />
  <button class="btn btn-primary">Verander wachtwoord</button>
</form>
