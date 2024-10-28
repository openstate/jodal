<script lang="ts">
  import { identity } from '$lib/stores';
  import { goto } from '$app/navigation';

  let errorMessage: false | string = $state(false);

  async function submit(e: SubmitEvent) {
    e.preventDefault();
    const node = e.target as HTMLFormElement;

    errorMessage = false;

    const response = await fetch(node.action, {
      method: node.method,
      body: new FormData(node),
      credentials: 'include',
      cache: 'no-cache',
    });

    const json = await response.json();

    if (response.status === 400) {
      errorMessage = 'Onjuist e-mailadres of wachtwoord.';
    }

    if (response.status === 200) {
      identity.set(json);
      goto('/');
    }
  }
</script>

<h1>Inloggen</h1>

{#if errorMessage}
  <div class="alert alert-danger" role="alert">
    {errorMessage}
  </div>
{/if}

<form method="POST" action="//api.bron.live/users/login" onsubmit={submit}>
  <input type="email" name="email" placeholder="E-mail" />
  <input type="password" name="password" placeholder="Wachtwoord" />
  <button class="btn btn-primary">Inloggen</button>
</form>

<a href="/forgot-password">Wachtwoord vergeten</a>
