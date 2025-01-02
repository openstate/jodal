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

<div class="grid grid-cols-[2fr_1fr] gap-16">
  <div class="space-y-4">
    <form
      onsubmit={(e) => (e.preventDefault(), (query.term = searchInput))}
      class="flex w-full items-center rounded-lg bg-white outline-2 outline-stone-200 transition-[outline] focus-within:outline-stone-300"
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
    </form>

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
  <aside class="space-y-6">
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
