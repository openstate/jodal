<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg";

  let { children } = $props();
</script>

<div class="max-w-300 fixed left-1/2 top-0 mx-auto w-full -translate-x-1/2 p-4">
  <nav
    class="flex w-full items-center justify-between rounded-2xl border border-stone-200 bg-white p-3"
  >
    <a href="/" class="px-3">
      <img src={BronLogo} class="h-8" alt="Bron Logo" />
    </a>
    <div class="flex gap-2 text-lg">
      <a
        href="/inloggen"
        class="font-stone-700 rounded-lg border border-stone-200 px-4 py-2"
      >
        Inloggen
      </a>
      <a
        href="/registreren"
        class="rounded-lg bg-purple-700 px-4 py-2 font-bold text-white"
      >
        Maak gratis account
      </a>
    </div>
  </nav>
</div>

<main class="pt-48">
  {@render children?.()}
</main>

<footer class="mt-12 text-center text-stone-500">
  <a href="/" class="font-medium hover:underline">Bron</a>
  is een initiatief van
  <a
    href="https://openstate.eu/nl"
    target="_blank"
    class="font-medium hover:underline"
  >
    Open State Foundation
  </a>.
</footer>
