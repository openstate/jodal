<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg?raw";

  let { data, children } = $props();
</script>

<main class="flex min-h-screen flex-col">
  <div
    class="max-w-300 absolute left-1/2 top-0 z-10 mx-auto w-full -translate-x-1/2 p-4"
  >
    <nav
      class="flex w-full items-center justify-between rounded-full border border-stone-300 bg-white p-3"
    >
      <a href="/" class="px-5">
        {@html BronLogo}
      </a>
      <div class="flex gap-2 md:text-lg">
        <a
          href={data.identity ? "/gids" : "/inloggen"}
          class="flex items-center rounded-full border border-stone-300 px-5 py-2 text-stone-800 transition hover:bg-stone-50 max-sm:hidden"
        >
          {#if data.identity}
            Ontdekken
          {:else}
            Inloggen
          {/if}
        </a>
        <a
          href={data.identity ? "/zoeken" : "/registreren"}
          class="flex items-center rounded-full bg-stone-900 px-6 py-2 font-semibold text-white transition hover:bg-stone-800"
        >
          {#if data.identity}
            <span class="max-sm:hidden">Begin met zoeken</span>
            <span class="sm:hidden">Zoeken</span>
          {:else}
            <span class="max-sm:hidden">Maak gratis account</span>
            <span class="sm:hidden">Aanmelden</span>
          {/if}
        </a>
      </div>
    </nav>
  </div>

  <div class="grow">
    {@render children?.()}
  </div>

  <footer class="rounded-t-3xl bg-stone-900 py-24 text-white">
    <div class="max-w-300 mx-auto px-6">
      <div class="mb-12 grid gap-4 sm:grid-cols-2 md:grid-cols-[1fr_25rem]">
        <a href="/" class="w-fit space-y-4">
          {@html BronLogo}
          <span class="text-lg text-stone-400">
            Superkrachten voor journalisten
          </span>
        </a>
        <div class="flex flex-col gap-2 font-semibold">
          <a href="/over">Over Bron</a>
          <a href="/over#heading-neem-contact-op">Contact</a>
          <a href="https://github.com/openstate/jodal" target="_blank">GitHub</a>
        </div>
      </div>
      <p class="text-stone-400">
        De content op deze site is beschikbaar onder de licentie
        <a
          href="https://creativecommons.org/licenses/by-sa/4.0/deed.nl"
          target="_blank"
          class="underline"
        >
          Creative Commons Naamsvermelding/Gelijk delen
        </a>, er kunnen aanvullende voorwaarden van toepassing zijn. Zie de
        gebruiksvoorwaarden voor meer informatie. Bron is onderdeel van
        <a href="https://openstate.eu/nl" target="_blank" class="underline">
          Open State Foundation
        </a>, een organisatie zonder winstoogmerk.
      </p>
    </div>
  </footer>
</main>
