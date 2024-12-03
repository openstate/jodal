<script lang="ts">
  let { data } = $props();
</script>

{#if data.identity}
  <div class="page">
    <p>Welkom, <b>{data.identity.email}</b>!</p>
  </div>
{:else}
  <p>
    Je bent momenteel niet ingelogd. Log in of registreer om Bron te gebruiken.
  </p>
{/if}
