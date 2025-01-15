<script lang="ts">
  import { allSources } from "$lib/sources";
  import { getQueryContext } from "./state.svelte";
  import type { PageData } from "./$types";
  import Select from "svelte-select";

  let { data }: { data: PageData } = $props();

  const query = getQueryContext();

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
</script>

<hr class="border-stone-200 max-md:hidden" />
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
        query.organisations = e.detail.map((v: { value: string }) => v.value);
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
  <p class="my-2 text-stone-700">Startdatum</p>
  <input
    type="date"
    bind:value={query.dateFrom}
    class={[
      "w-full rounded-lg border-2 border-stone-200 bg-white px-4 py-3 outline-0 transition focus-within:border-stone-300",
      query.dateFrom ? "text-stone-800" : "text-stone-500",
    ]}
  />
  <p class="my-2 text-stone-700">Einddatum</p>
  <input
    type="date"
    bind:value={query.dateTo}
    class={[
      "w-full rounded-lg border-2 border-stone-200 bg-white px-4 py-3 outline-0 transition focus-within:border-stone-300",
      query.dateTo ? "text-stone-800" : "text-stone-500",
    ]}
  />
</div>
<hr class="border-stone-200" />
