<script lang="ts">
  import ArrowRight from "@tabler/icons-svelte/icons/arrow-right";

  let { data } = $props();
</script>

<section class="max-w-300 mx-auto">
  <h1 class="font-display pt-10 text-center text-6xl font-bold">
    Superkrachten voor journalisten
  </h1>
  <h2 class="mt-8 text-center text-2xl font-light text-stone-700">
    Onderzoek 13 miljoen overheidsdocumenten op één plek
  </h2>
  <form
    action="/zoeken"
    class="max-w-150 mx-auto mt-16 flex items-center justify-between rounded-lg border border-stone-300 bg-white text-lg focus-within:border-stone-400"
  >
    <input
      type="search"
      name="zoek"
      placeholder="Zoek over elk onderwerp..."
      class="w-full px-6 py-4 text-xl placeholder:text-stone-400 focus:outline-0"
    />
    <button
      class="mx-2.5 flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-lg bg-purple-700 text-white"
    >
      <ArrowRight />
    </button>
  </form>
  <div
    class="max-w-150 max-h-22 mx-auto mt-6 flex flex-wrap justify-center gap-2 overflow-y-hidden"
  >
    {#each data.examples as example}
      <a
        href="/zoeken?zoek={example.query}"
        class="flex h-10 items-center gap-2 rounded-lg border border-stone-300 bg-white px-3 py-2 font-light text-stone-700"
      >
        <span>{example.emoji}</span>
        {example.name}
      </a>
    {/each}
  </div>
</section>
