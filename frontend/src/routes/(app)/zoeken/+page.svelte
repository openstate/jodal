<script lang="ts">
  import {
    IconBookmark,
    IconFilter,
    IconPlus,
    IconSearch,
  } from "@tabler/icons-svelte";

  import Document from "$lib/components/document.svelte";
  import SkeletonDocument from "$lib/components/skeleton-document.svelte";
  import MakeFeed from "./make-feed.svelte";
  import Filters from "./filters.svelte";

  import { createQueryState } from "./state.svelte";
  import { debounce } from "$lib/utils";
  import { dev } from "$app/environment";

  let { data } = $props();

  const query = createQueryState();

  let searchInput = $state(query.term);

  const setQueryTerm = debounce((v) => {
    if (v !== query.term) query.term = v;
  }, 500);

  $effect(() => setQueryTerm(searchInput));

  const numberFormatter = new Intl.NumberFormat("nl-NL");

  if (dev) $inspect(data.documents).with(async (_, d) => console.log(await d));

  let filtersOpen = $state(false);
  let newFeedsOpen = $state(false);
</script>

<div class="md:grid md:grid-cols-[2fr_1fr] md:gap-8 md:py-4 xl:gap-12">
  <div>
    <form
      class="border-stone-200 bg-stone-50 max-md:sticky max-md:-top-4 max-md:-m-4 max-md:w-screen max-md:border-b-2 max-md:p-4"
    >
      <div
        onsubmit={(e) => (e.preventDefault(), (query.term = searchInput))}
        class="flex w-full items-center rounded-lg border-2 border-stone-200 bg-white outline-0 transition focus-within:border-stone-300"
      >
        <!-- svelte-ignore a11y_autofocus -- search is legitimate use of autofocus -->
        <input
          autofocus={true}
          class="grow rounded-lg border-0 px-4 py-3 outline-0 ring-0"
          type="search"
          name="zoek"
          placeholder="Zoek documenten..."
          bind:value={searchInput}
        />
        <button type="submit" class="mx-2 cursor-pointer p-2">
          <IconSearch />
        </button>
      </div>

      <div class="mt-2 flex justify-between gap-3 md:hidden">
        <button
          class="flex grow items-center justify-center gap-1.5 rounded-lg border-2 border-stone-200 bg-white px-2.5 py-1.5 text-stone-800"
          onclick={() => (filtersOpen = !filtersOpen)}
          type="button"
        >
          <IconFilter class="-ml-1 size-4" />
          Filter
        </button>
        <button
          class="flex grow items-center justify-center gap-1.5 rounded-lg bg-purple-200/80 px-2.5 py-1.5 text-purple-900"
          onclick={() => (newFeedsOpen = true)}
          type="button"
        >
          <IconBookmark class="-ml-1 size-4" />
          Bewaar
        </button>
      </div>
    </form>

    <div class="mt-10 space-y-4 md:mt-6">
      {#await data.documents}
        <div class="my-5 h-4 w-36 animate-pulse rounded-lg bg-stone-200"></div>
        {#each { length: 20 } as _}
          <SkeletonDocument />
        {/each}
      {:then documents}
        <p>
          {#if documents.hits.total.value === 0}
            Geen resultaten
          {:else}
            {numberFormatter.format(
              documents.hits.total.value,
            )}{#if documents.hits.total.relation === "gte"}+{/if}
            {#if documents.hits.total.value === 1}resultaat{:else}resultaten{/if}
          {/if}
        </p>

        {#each documents?.hits.hits ?? [] as document}
          <Document {document} />
        {/each}
      {/await}
    </div>
  </div>
  <aside
    class={[
      "max-md:top-50 space-y-6 bg-stone-50 duration-300 max-md:fixed max-md:inset-0 max-md:overflow-y-scroll max-md:p-6",
      !filtersOpen && "max-md:translate-x-full",
    ]}
  >
    <button
      class="flex cursor-pointer items-center gap-4 rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:cursor-auto disabled:opacity-20 max-md:hidden"
      onclick={() => (newFeedsOpen = true)}
    >
      <IconPlus class="w-5" />
      Sla zoekopdracht op
    </button>

    <Filters {data} />

    <button
      class="flex w-full cursor-pointer items-center justify-center gap-4 rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:cursor-auto disabled:opacity-20 md:hidden"
      onclick={() => (filtersOpen = false)}
    >
      Filters toepassen
    </button>
  </aside>
</div>

<MakeFeed bind:open={newFeedsOpen} />
