<script lang="ts">
  import { enhance } from '$app/forms';

  let { form } = $props();
</script>

<h1>Inloggen</h1>

{#if form?.success === false}
  <div class="alert alert-danger">
    <p>{form.message}</p>
  </div>
{/if}

<form method="POST" use:enhance>
  <input type="email" name="email" placeholder="E-mail" />
  <input type="password" name="password" placeholder="Wachtwoord" />
  <button class="btn btn-primary">Inloggen</button>
</form>

<a href="/forgot-password">Wachtwoord vergeten</a>
