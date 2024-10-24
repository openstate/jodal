<script lang="ts">
  let successMessage: false | string = $state(false);
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

    if (response.status === 400) {
      errorMessage = 'Onjuist e-mailadres of wachtwoord.';
    }

    if (response.status === 200) {
      successMessage = 'Check je e-mail om je registratie te bevestigen.';
    }
  }
</script>

<h1>Registreren</h1>

{#if errorMessage}
  <div class="alert alert-danger" role="alert">
    {errorMessage}
  </div>
{/if}

{#if successMessage}
  <div class="alert alert-success" role="alert">
    {successMessage}
  </div>
{/if}


<form method="POST" action="//api.bron.live/users/register" onsubmit={submit}>
  <input type="email" name="email" placeholder="E-mail" />
  <input type="password" name="password" placeholder="Wachtwoord" />
  <button class="btn btn-primary">Registreren</button>
</form>
