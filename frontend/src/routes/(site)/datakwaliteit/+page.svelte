<script lang="ts">
  import { allSources } from "$lib/sources";

  const { format: formatNumber } = new Intl.NumberFormat("nl-NL");
  const { format: formatDate } = new Intl.DateTimeFormat("nl-NL", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  let { data } = $props();
</script>

<svelte:head>
  <title>Datakwaliteit &ndash; Bron</title>
</svelte:head>

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
      Datakwaliteit
    </h1>
    <h2 class="text-balance text-xl text-stone-100/80 sm:text-2xl">
      Wat zit er in Bron? En wat mist er nog?
    </h2>
  </div>
</header>

<div
  class="max-w-300 mx-auto grid gap-10 px-6 py-12 lg:grid-cols-[1fr_20rem] lg:pt-16"
>
  <div
    class="col-span-2 overflow-x-auto rounded-lg border border-stone-300 bg-white px-6 py-5"
  >
    {#await data.aggregations then aggregations}
      <table class="w-full">
        <thead>
          <tr>
            <th class="px-2 py-4 text-left font-semibold">Naam</th>
            <th class="px-2 py-4 text-left font-semibold">
              Aantal documenten
            </th>
            <th class="px-2 py-4 text-left font-semibold"> Eerste document </th>
            <th class="px-2 py-4 text-left font-semibold">
              Laatste document
            </th>
            <th class="px-2 py-4 text-left font-semibold">
              Documenten per maand
            </th>
          </tr>
        </thead>
        <tbody>
          {#each allSources as { label, value }}
            {@const source = aggregations[value]}
            <tr class="group">
              {@render td(label)}

              {#if source}
                {@render td(formatNumber(source.total_documents))}
                {@render td(formatDate(new Date(source.first_date)))}
                {@render td(formatDate(new Date(source.last_date)))}
                {@render td()}
              {:else}
                {@render td()}
                {@render td()}
                {@render td()}
                {@render td()}
              {/if}
            </tr>
          {/each}
        </tbody>
      </table>
    {/await}
  </div>
</div>

{#snippet th(content: string)}
  <th class="border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0">
    {content}
  </th>
{/snippet}

{#snippet td(content?: string)}
  <td
    class={[
      "border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0",
      !content && "text-stone-400",
    ]}
  >
    {#if content}{content}{:else}&mdash;{/if}
  </td>
{/snippet}
