<script lang="ts">
  import { enhance } from '$app/forms';
  import { page } from '$app/stores';

  const id = $derived($page.url.searchParams.get('id'));

  let { form } = $props();
</script>

<h1>Wachtwoord veranderen</h1>

{#if form?.message || !id}
  <div class="alert alert-danger">
    {#if !id}
      <p>Je kan niet je wachtwoord veranderen zonder geldige code.</p>
    {:else}
      <p>{form?.message}</p>
    {/if}
  </div>
{/if}

<form method="POST" use:enhance>
  <input type="hidden" name="changePasswordId" value={id} />
  <input type="password" name="password" placeholder="Nieuw wachtwoord" />
  <input
    type="password"
    name="password_repeat"
    placeholder="Herhaal nieuw wachtwoord"
  />
  <button class="btn btn-primary">Verander wachtwoord</button>
</form>
