<script lang="ts">
  let successMessage: false | string = $state(false);

  async function submit(e: SubmitEvent) {
    e.preventDefault();
    const node = e.target as HTMLFormElement;

    successMessage = false;

    const response = await fetch(node.action, {
      method: node.method,
      body: new FormData(node),
      cache: 'no-cache',
    });

    const json = await response.json();

    console.log(json)

    if (json.success) {
      successMessage = "Bevestigingsmail verstuurd.";
    }
  }
</script>

<h1>Wachtwoord vergeten</h1>

{#if successMessage}
  <div class="alert alert-success" role="alert">
    {successMessage}
  </div>
{/if}

<form method="POST" action="//api.bron.live/users/forgot-password" onsubmit={submit}>
  <input type="email" name="email" placeholder="E-mail" />
  <button class="btn btn-primary">Verstuur bevestigingsmail</button>
</form>