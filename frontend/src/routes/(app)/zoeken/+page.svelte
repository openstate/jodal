<script lang="ts">
  import Search from "@tabler/icons-svelte/icons/search";
  import Select from "svelte-select";

  import Document from "$lib/components/document.svelte";
  import SkeletonDocument from "$lib/components/skeleton-document.svelte";
  import DateInput from "$lib/components/date-input.svelte";
  import MakeFeed from "$lib/components/make-feed.svelte";

  import { allSources } from "./sources";
  import { createQueryState } from "./state.svelte";
  import { debounce } from "$lib/utils";
  import { dev } from "$app/environment";
  import {
    IconBookmark,
    IconFilter,
    IconFilterFilled,
  } from "@tabler/icons-svelte";

  let { data } = $props();

  const query = createQueryState();

  let searchInput = $state(query.term);

  const setQueryTerm = debounce((v) => {
    if (v !== query.term) query.term = v;
  }, 500);

  $effect(() => setQueryTerm(searchInput));

  function onSourceChange(value: string, checked: boolean) {
    if (value === "*") query.sources = [];
    else if (checked) query.sources.push(value);
    else query.sources = query.sources.filter((v) => v !== value);
  }

  const organisationItems = $derived.by(async () =>
    (await data.locations).hits.hits.map((hit) => ({
      value: hit._source.id,
      label: hit._source.name,
    })),
  );

  const numberFormatter = new Intl.NumberFormat("nl-NL");

  const countBySource = $derived.by(async () =>
    (await data.aggregations).aggregations.source.buckets.reduce(
      (acc, bucket) => ({ ...acc, [bucket.key]: bucket.doc_count }),
      {} as Record<string, number>,
    ),
  );

  if (dev) $inspect(data.documents).with(async (_, d) => console.log(await d));
</script>

<div class="md:grid md:grid-cols-[2fr_1fr] md:py-4 md:gap-8 xl:gap-12">
  <div>
    <form
      class="border-stone-200 bg-stone-50 max-md:p-4 max-md:sticky max-md:-top-4 max-md:-m-4 max-md:w-screen max-md:border-b-2"
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
          <Search />
        </button>
      </div>

      <div class="mt-2 flex justify-between gap-3 md:hidden">
        <button
          class="flex grow items-center justify-center gap-1.5 rounded-lg border-2 border-stone-200 bg-white px-2.5 py-1.5 text-stone-800"
        >
          <IconFilter class="-ml-1 size-4" />
          Filter
        </button>
        <!-- <div class="border-r-2 border-stone-200"></div> -->
        <button
          class="flex grow items-center justify-center gap-1.5 rounded-lg bg-purple-200/80 px-2.5 py-1.5 text-purple-900"
        >
          <IconBookmark class="-ml-1 size-4" />
          Bewaar
        </button>
      </div>
    </form>

    <div class="mt-10 md:mt-6 space-y-4">
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
  <aside class="space-y-6 max-md:hidden">
    <MakeFeed {query} />
    <hr class="border-stone-200" />
    <div class="space-y-1">
      <h2 class="mb-3 font-bold">Bronnen</h2>
      <div class="flex items-center gap-2">
        <input
          type="checkbox"
          id="all-sources"
          name="*"
          checked={query.sources.length === allSources.length}
          onchange={(e) =>
            onSourceChange(e.currentTarget.name, e.currentTarget.checked)}
        />
        <label for="all-sources">Alle bronnen</label>
      </div>
      {#each allSources as source}
        <div class="flex items-center gap-2">
          <input
            type="checkbox"
            id={source.value}
            name={source.value}
            checked={query.sources.includes(source.value)}
            onchange={(e) =>
              onSourceChange(e.currentTarget.name, e.currentTarget.checked)}
          />
          <label for={source.value} class="flex gap-2">
            <div>{source.label}</div>
            {#await countBySource then countBySource}
              {#if countBySource[source.value] > 0}
                <div
                  class="rounded-full bg-purple-100/80 px-2.5 py-0.5 text-sm text-purple-950"
                >
                  {numberFormatter.format(countBySource[source.value])}
                </div>
              {/if}
            {/await}
          </label>
        </div>
      {/each}
    </div>
    <hr class="border-stone-200" />
    <div class="space-y-1">
      <h2 class="mb-3 font-bold">Organisaties</h2>
      {#await organisationItems}
        <Select multiple placeholder="Zoek organisaties..." />
      {:then organisationItems}
        <Select
          multiple
          placeholder="Zoek organisaties..."
          items={organisationItems}
          value={organisationItems.filter((item) =>
            query.organisations.includes(item.value),
          )}
          on:change={(e) => {
            query.organisations = e.detail.map(
              (v: { value: string }) => v.value,
            );
          }}
          on:clear={(e) => {
            query.organisations = query.organisations.filter(
              (v) => v !== e.detail.value,
            );
          }}
        />
      {/await}
    </div>
    <hr class="border-stone-200" />
    <div class="space-y-1">
      <h2 class="mb-3 font-bold">Datum</h2>
      <div class="flex items-center gap-2">
        <DateInput bind:value={query.dateFrom} placeholder="Startdatum" />
        <span class="px-2 text-stone-600">&mdash;</span>
        <DateInput bind:value={query.dateTo} placeholder="Einddatum" />
      </div>
    </div>
    <hr class="border-stone-200" />
  </aside>
</div>
