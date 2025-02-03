<script lang="ts">
  let { data } = $props();
</script>

<div class="px-6 py-36 md:py-48">
  <div
    class="max-w-120 m-2 mx-auto mt-20 w-full space-y-4 rounded-lg border border-stone-300 bg-white p-8"
  >
    <p>
      {#if data.success}
        Je hebt je succesvol afgemeld voor mails van deze feed.
      {:else}
        Er is iets misgegaan bij het afmelden voor mails van deze feed. Probeer
        het later opnieuw.
      {/if}
    </p>
    <a
      href={data.identity ? "/" : "/inloggen"}
      class="block w-fit cursor-pointer rounded-lg bg-stone-900 px-4 pb-2 pt-2 font-bold text-white transition hover:bg-stone-800"
    >
      {#if data.identity}
        Ga naar Bron
      {:else}
        Inloggen
      {/if}
    </a>
  </div>
</div>
