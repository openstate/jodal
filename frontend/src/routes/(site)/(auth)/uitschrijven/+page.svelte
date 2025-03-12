<script lang="ts">
  let { data } = $props();
</script>

<svelte:head>
  <title>Uitschrijven &ndash; Bron</title>
</svelte:head>

<div
  class="max-w-120 m-2 mx-auto mt-20 w-full space-y-4 rounded-lg border border-stone-300 bg-white p-8"
>
  <h1 class="mb-2 text-lg font-medium">
    Je bent {#if !data.success}niet{" "}{/if} uitgeschreven voor Bron alerts
  </h1>

  <p class="text-stone-700">
    {#if data.success}
      Je ontvangt voortaan geen e-mails meer van Bron. Je kunt je altijd weer
      inschrijven voor meldingen door een nieuwe feed aan te maken.
    {:else}
      Er is iets misgegaan bij het uitschrijven. Probeer het later nog eens. Als
      het probleem zich blijft voordoen, neem dan contact op via
      <a href="mailto:contact@openstate.eu" class="underline">
        contact@openstate.eu
      </a>.
    {/if}
  </p>

  <a
    href="/"
    class="block w-fit cursor-pointer rounded-lg bg-stone-900 px-4 pb-2 pt-2 font-bold text-white transition hover:bg-stone-800"
  >
    Terug naar homepagina
  </a>
</div>
