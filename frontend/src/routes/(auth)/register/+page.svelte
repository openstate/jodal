<script lang="ts">
  import { enhance } from '$app/forms';

  let { form } = $props();
</script>

<h1>Registreren</h1>

{#if form?.message}
  <div class="alert alert-success" class:alert-danger={form.success === false}>
    <p>{form.message}</p>
  </div>
{/if}

<form method="POST" use:enhance>
  <input type="email" name="email" placeholder="E-mail" />
  <input type="password" name="password" placeholder="Wachtwoord" />
  <button class="btn btn-primary">Registreren</button>
</form>
