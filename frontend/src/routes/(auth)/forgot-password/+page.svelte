<script lang="ts">
  import { enhance } from '$app/forms';

  let { form } = $props();
</script>

<h1>Wachtwoord vergeten</h1>

{#if form?.message}
  <div class="alert alert-success" class:alert-danger={form.success === false}>
    <p>{form.message}</p>
  </div>
{/if}

<form method="POST" use:enhance>
  <input type="email" name="email" placeholder="E-mail" />
  <button class="btn btn-primary">Verstuur bevestigingsmail</button>
</form>
