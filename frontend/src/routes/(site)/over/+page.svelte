<script lang="ts">
  import LandingCTA from "$lib/components/landing/cta.svelte";

  let { data } = $props();
</script>

<header class="h-100 md:h-120 relative overflow-hidden">
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
      Over Bron
    </h1>
    <h2 class="text-balance text-xl text-stone-100/80 sm:text-2xl">
      Wat is Bron? Hoe werkt het? En wat beweegt ons?
    </h2>
  </div>
</header>

<div
  class="max-w-300 mx-auto grid gap-10 px-6 pt-12 lg:grid-cols-[1fr_20rem] lg:pt-16"
>
  <article class="prose prose-stone mx-auto max-w-full max-lg:order-1">
    {@html data.markdown}
  </article>

  <div
    class="max-lg:order-0 h-fit rounded border border-stone-300 bg-white p-6 text-stone-700"
  >
    <h2 class="mb-3 text-lg font-bold">Op deze pagina</h2>

    <ul class="flex list-inside list-disc max-lg:flex-wrap lg:flex-col gap-x-6 gap-y-3">
      {#each data.headings as heading}
        <li>
          <a href="#{heading.id}" class="text-stone-800 underline">
            {heading.text}
          </a>
        </li>
      {/each}
    </ul>
  </div>
</div>

<LandingCTA />
