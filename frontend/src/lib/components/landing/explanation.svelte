<script lang="ts">
  import { IconBookmarkFilled, IconSearch } from "@tabler/icons-svelte";

  let steps = [
    {
      snippet: search,
      title: "Zoek",
      description:
        "Wij checken meer dan 2 miljoen documenten op jouw zoektermen.",
    },
    {
      snippet: filter,
      title: "Filter",
      description:
        "Vind precies de documenten die voor jouw werk belangrijk zijn.",
    },
    {
      snippet: feed,
      title: "Monitor",
      description:
        "Sla je opdracht op als feed en krijg een mail bij nieuwe documenten.",
    },
  ];
</script>

<article class="my-30 px-6 text-stone-800">
  <h2 class="font-display mb-4 text-balance text-center text-4xl">
    Mis nooit meer dat ene document
  </h2>
  <h3 class="max-w-150 mx-auto text-balance text-center text-xl text-stone-500">
    In drie stappen weet je altijd wat er speelt in jouw regio.
  </h3>

  <div class="max-w-300 mx-auto my-16 grid gap-6 md:grid-cols-3">
    {#each steps as step}
      <a
        href="/zoeken"
        class="rounded-2xl border border-stone-300 bg-gradient-to-tr from-white/60 to-white/20 p-8 transition hover:bg-stone-100"
      >
        <div class="min-h-40 md:min-h-50 relative">
          <div class="-translate-1/2 absolute left-1/2 top-1/2 max-w-[75%]">
            {@render step.snippet()}
          </div>
        </div>
        <div>
          <h4 class="font-display mb-2 text-xl font-medium">{step.title}</h4>
          <p class="font-stone-600 text-balance">{step.description}</p>
        </div>
      </a>
    {/each}
  </div>
</article>

{#snippet search()}
  <div
    class="flex w-full items-center rounded-lg border border-stone-300 bg-white outline-0 transition focus-within:border-stone-300"
  >
    <div
      class="grow truncate rounded-lg border-0 px-4 py-3 text-stone-500 outline-0 ring-0"
    >
      Zoek documenten...
    </div>
    <button type="submit" class="mx-2 p-2 text-stone-700">
      <IconSearch />
    </button>
  </div>
{/snippet}

{#snippet filter()}
  <div class="w-max space-y-2">
    {#each ["Provincie Overijssel", "Gemeente Zwolle", "Gemeente Enschede"] as tag}
      <div class="flex items-center gap-2">
        <input type="checkbox" checked onclick={(e) => e.preventDefault()} />
        <span>{tag}</span>
      </div>
    {/each}
  </div>
{/snippet}

{#snippet feed()}
  <button
    class="mb-4.5 flex w-max cursor-pointer items-center gap-2 rounded-lg bg-stone-800 px-4 py-3 font-semibold text-white"
  >
    <IconBookmarkFilled class="size-5" />
    Bewaar <span class="max-lg:hidden">zoekopdracht</span>
  </button>
{/snippet}
