<script lang="ts">
  import { page } from "$app/state";
  import type { getRandomExamples } from "$lib/examples";
  import ArrowRight from "@tabler/icons-svelte/icons/arrow-right";

  type Props = { examples: ReturnType<typeof getRandomExamples> };

  let { examples }: Props = $props();
</script>

<header class="h-170 md:h-190 relative overflow-hidden">
  <enhanced:img
    src="$lib/assets/hero.png?quality=90"
    sizes="min(1280px, 100vw)"
    fetchpriority="high"
    class="absolute inset-x-0 h-full w-full object-cover"
  />
  <div
    class="-translate-1/2 absolute left-1/2 top-1/2 w-full px-6 pt-20 text-center"
  >
    <h1
      class="font-display mb-4 text-balance text-4xl font-medium text-white sm:mb-8 sm:text-5xl sm:font-normal md:text-6xl"
    >
      Superkrachten voor journalisten
    </h1>
    <h2 class="text-balance text-xl text-stone-100/80 sm:text-2xl">
      Doorzoek meer dan 2 miljoen overheidsdocumenten op één plek.
    </h2>
    <form
      action="/zoeken"
      class="max-w-150 focus-within:outline-3 mx-auto mt-16 flex items-center justify-between rounded-full bg-white focus-within:outline-white/50 sm:text-lg"
    >
      <input
        type="search"
        name="zoek"
        placeholder="Zoek over elk onderwerp..."
        class="sm:pb-4.5 w-full px-6 py-3 placeholder:text-stone-400 focus:outline-0 sm:px-8 sm:py-4 sm:text-xl"
      />
      <button
        class="mx-1 sm:mx-2 flex sm:h-12 sm:w-12 w-10 h-10 shrink-0 cursor-pointer items-center justify-center rounded-full bg-stone-900 text-white transition hover:bg-stone-800"
      >
        <ArrowRight />
      </button>
    </form>
    <div
      class="max-w-120 mx-auto mt-6 flex max-h-24 flex-wrap justify-center gap-x-3 gap-y-3.5 overflow-y-hidden"
    >
      {#each examples as example}
        <a
          href="/zoeken?zoek={example.query}"
          class="flex h-10 items-center rounded-full border border-white/40 bg-white/30 px-3 sm:px-4 sm:py-2 font-medium text-white backdrop-blur-sm transition hover:bg-white/35 max-sm:text-sm"
        >
          {example.name}
        </a>
      {/each}
    </div>
  </div>
</header>
