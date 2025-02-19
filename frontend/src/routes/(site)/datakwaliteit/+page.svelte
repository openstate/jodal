<script lang="ts">
  import { allSources } from "$lib/sources";
  import { IconChevronDown } from "@tabler/icons-svelte";
  import Sparkbar from "./sparkbar.svelte";
  import { goto } from "$app/navigation";
  import { getLocationItems } from "$lib/loaders";
  import { page } from "$app/state";

  const { format: formatNumber } = new Intl.NumberFormat("nl-NL");
  const { format: formatDate } = new Intl.DateTimeFormat("nl-NL", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  let { data } = $props();

  const locationItems = $derived(getLocationItems(data.locations));

  let organisationId = $state(page.url.searchParams.get("organisatie") ?? "*");

  $effect(() => {
    goto(`/datakwaliteit?organisatie=${organisationId}`);
  });
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
    <div
      class="mb-2 flex w-fit items-center gap-2 rounded-lg border border-zinc-300"
    >
      <select
        class="appearance-none py-2 pl-3"
        onchange={(e) => (organisationId = e.currentTarget.value)}
      >
        {#each locationItems as location}
          <option
            value={location.value}
            selected={location.value === organisationId}
          >
            {#if location.value === "*"}Alle organisaties{:else}{location.label}{/if}
          </option>
        {/each}
      </select>
      <IconChevronDown class="mr-3 size-5" />
    </div>

    <table class="min-w-250 w-full">
      <thead>
        <tr>
          {@render cell_heading("Naam")}
          {@render cell_heading("Aantal documenten")}
          {@render cell_heading("Eerste document")}
          {@render cell_heading("Laatste document")}
          {@render cell_heading("Documenten per kwartaal")}
        </tr>
      </thead>
      <tbody>
        {#each allSources as { label, value }}
          <tr class="group">
            {@render cell(label)}

            {#await data.aggregations}
              {@render cell_skeleton()}
              {@render cell_skeleton()}
              {@render cell_skeleton()}
              {@render cell_skeleton()}
            {:then aggregations}
              {@const source = aggregations[value]}
              {#if source}
                {@render cell(formatNumber(source.total_documents))}
                {@render cell(formatDate(new Date(source.first_date)))}
                {@render cell(formatDate(new Date(source.last_date)))}
                <td
                  class="h-4 border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0"
                >
                  <Sparkbar data={source.quarterly_documents} />
                </td>
              {:else}
                {@render cell()}
                {@render cell()}
                {@render cell()}
                {@render cell()}
              {/if}
            {/await}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

{#snippet cell_heading(content: string)}
  <th class="border-b border-stone-300 px-2 py-4 text-left">
    {content}
  </th>
{/snippet}

{#snippet cell(content?: string)}
  <td
    class={[
      "border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0",
      !content && "text-stone-400",
    ]}
  >
    {#if content}{content}{:else}&mdash;{/if}
  </td>
{/snippet}

{#snippet cell_skeleton()}
  <td class="border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0">
    <div class="h-4 animate-pulse rounded bg-stone-200"></div>
  </td>
{/snippet}
