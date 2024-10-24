<script lang="ts">
  let errorMessage: false | string = $state(false);

  async function submit(e: SubmitEvent) {
    e.preventDefault();
    const node = e.target as HTMLFormElement;

    errorMessage = false;

    const response = await fetch(node.action, {
      method: node.method,
      body: new FormData(node),
      cache: 'no-cache',
    });

    const json = await response.json();

    console.log(json)
  }
</script>

<h1>Wachtwoord vergeten</h1>

{#if errorMessage}
  <div class="alert alert-danger" role="alert">
    {errorMessage}
  </div>
{/if}

<form method="POST" action="//api.bron.live/users/forgot-password" onsubmit={submit}>
  <input type="email" name="email" placeholder="E-mail" />
  <button class="btn btn-primary">Verstuur bevestigingsmail</button>
</form>