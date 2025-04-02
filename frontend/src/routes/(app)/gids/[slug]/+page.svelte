<script lang="ts">
  import { page } from "$app/state";
  import ArrowRight from "@tabler/icons-svelte/icons/arrow-right";
  import LandingCTA from "$lib/components/landing/cta.svelte";

  let { data } = $props();
</script>

<svelte:head>
  <title>{data.attributes.title} &ndash; Bron</title>
</svelte:head>

<div class="relative mb-6 h-80">
  <img
    src={data.attributes.image}
    alt={data.attributes.title}
    fetchpriority="high"
    class="absolute inset-0 h-full w-full object-cover"
  />
  <div
    class="backdrop-blur-xs absolute inset-0 bg-gradient-to-t from-black/70 from-20% to-black/10"
  ></div>
  <div
    class="absolute bottom-12 left-1/2 -translate-x-1/2 sm:bottom-16 xl:[translate:calc(-12.25rem_-_50%)_0]"
  >
    <h1 class="font-display mb-4 text-center text-4xl text-white">
      {data.attributes.title}
    </h1>
    <p class="text-balance text-center text-lg text-stone-200/90 sm:text-xl">
      {data.attributes.description}
    </p>
  </div>
</div>

<div class="max-w-300 mx-auto grid gap-10 px-6 py-8 xl:grid-cols-[1fr_20rem]">
  <div>
    <article
      class={[
        "prose prose-stone relative max-w-full",
        !page.data.identity && "max-h-150 overflow-y-hidden",
      ]}
    >
      {@html data.body}

      {#if !page.data.identity}
        <div
          class="pointer-events-none absolute inset-0 bg-gradient-to-t from-stone-50 from-5% to-stone-50/0 to-30%"
        ></div>
      {/if}
    </article>

    {#if !page.data.identity}
      <div class="-my-20">
        <LandingCTA title="Verder lezen? Sluit je aan bij Bron" />
      </div>
    {/if}
  </div>
  <div
    class="h-fit rounded border border-stone-300 bg-white p-6 text-stone-800"
  >
    <p class="mb-2 text-lg font-medium text-stone-900">Verder zoeken</p>
    <p class="mb-4">
      Gebruik Bron voor jouw onderzoek over {data.attributes.title.toLocaleLowerCase()}
      om de laatste overheidsdocumenten te vinden.
    </p>
    <div class="flex flex-wrap gap-2">
      {#each data.attributes.feeds as feed}
        <a
          href="/zoeken?zoek={feed}"
          class="ml-au flex w-fit items-center gap-2 rounded-full bg-blue-100 px-3 py-0.5 capitalize text-blue-900"
        >
          <ArrowRight class="size-4" /> {feed}</a
        >
      {/each}
    </div>
  </div>
</div>
