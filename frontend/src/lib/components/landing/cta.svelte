<script lang="ts">
  import { page } from "$app/state";

  let { title }: { title?: string } = $props();
</script>

<article class="my-30 px-6 py-10 text-stone-800">
  <h2 class="font-display mb-4 text-balance text-center text-4xl">
    {title ?? "Sluit je aan bij Bron"}
  </h2>

  <h3
    class="max-w-150 mx-auto mb-12 text-balance text-center text-xl text-stone-500"
  >
    Stel geavanceerde zoekopdrachten in en ontvang nieuwe zoekresultaten in je
    e-mail.
  </h3>

  <a
    href={page.data.identity ? "/zoeken" : "/registreren"}
    class="mx-auto mb-4 flex w-fit items-center rounded-full bg-stone-900 px-6 py-3 text-xl font-semibold text-white transition hover:bg-stone-800"
  >
    {#if page.data.identity}Begin met zoeken{:else}Maak een gratis account aan{/if}
  </a>

  {#if !page.data.identity}
    <p class="text-center text-lg text-stone-500">
      Heb je al een account?
      <a href="/inloggen" class="text-stone-600 underline">Log in</a>.
    </p>
  {/if}
</article>
