<script lang="ts">
  let { data } = $props();
</script>

<svelte:head>
  <title>Registratie bevestigen &ndash; Bron</title>
</svelte:head>

<div
  class="max-w-120 m-2 mx-auto mt-20 w-full space-y-4 rounded-lg border border-stone-300 bg-white p-8"
>
  <h1 class="mb-2 text-lg font-medium">
    Je e-mail is {#if !data.success}niet{" "}{/if}bevestigd
  </h1>

  <p class="text-stone-700">
    {#if data.success}
      Jouw email is bevestigd! Dat betekent dat je nu kunt inloggen op Bron.
    {:else}
      Jouw e-mail kon helaas niet worden bevestigd. Mogelijk heb je je e-mail
      eerder al bevestigd. Probeer in te loggen.
    {/if}
  </p>

  <a
    href="/inloggen"
    class="block w-fit cursor-pointer rounded-lg bg-stone-900 px-4 pb-2 pt-2 font-bold text-white transition hover:bg-stone-800"
  >
    Inloggen
  </a>
</div>
