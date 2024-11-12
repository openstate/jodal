<script lang="ts">
  import { identity } from '$lib/stores';
  import { enhance } from '$app/forms';
</script>

{#if $identity}
  <div class="page">
    <p>Welkom, <b>{$identity.email}</b>!</p>
    <ul>
      <li><a href="/dossiers/">Dossiers</a></li>
      <li><a href="/archief/">Archief</a></li>
      <li>...</li>
    </ul>
  </div>
  <form action="/logout" method="POST" use:enhance>
    <button class="btn btn-primary">Uitloggen</button>
  </form>
{:else}
  <p>
    Je bent momenteel niet ingelogd. Druk op de knop hieronder om naar de login
    pagina te gaan, of maak een account aan.
  </p>
  <a href="/login" class="btn btn-primary">Inloggen</a>
  <a href="/register" class="btn btn-primary">Registreren</a>
{/if}
