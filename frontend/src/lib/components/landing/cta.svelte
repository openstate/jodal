<script lang="ts">
  import { page } from "$app/state";
</script>

<article class="my-30 px-6 text-stone-800">
  <h2 class="font-display mb-4 text-balance text-center text-4xl">
    Mis nooit meer dat ene document
  </h2>

  <h3
    class="max-w-150 mx-auto mb-12 text-balance text-center text-xl text-stone-500"
  >
    Stel geavanceerde zoekopdrachten in en ontvang nieuwe zoekresultaten in je
    e-mail. {#if !page.data.identity}Maak een account aan.{/if}
  </h3>

  <a
    href={page.data.identity ? "/zoeken" : "/registreren"}
    class="mx-auto mb-4 flex w-fit items-center rounded-full bg-stone-900 px-6 py-3 text-xl font-semibold text-white transition hover:bg-stone-800"
  >
    {#if page.data.identity}Begin met zoeken{:else}Maak een gratis account aan{/if}
  </a>

  <p class="text-center text-stone-500">Exclusief voor journalisten</p>
</article>
