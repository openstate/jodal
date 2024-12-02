<script lang="ts">
  import { identity } from "$lib/stores";
</script>

{#if $identity}
  <div class="page">
    <p>Welkom, <b>{$identity.email}</b>!</p>
  </div>
{:else}
  <p>
    Je bent momenteel niet ingelogd. Log in of registreer om Bron te gebruiken.
  </p>
{/if}
