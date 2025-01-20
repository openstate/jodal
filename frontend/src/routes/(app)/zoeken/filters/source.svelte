<script lang="ts">
  import { allSources } from "$lib/sources";
  import { getQueryContext } from "../state.svelte";
  import type { PageData } from "../$types";
  const { format: formatNumber } = new Intl.NumberFormat("nl-NL");

  let { data }: { data: PageData } = $props();

  const query = getQueryContext();

  const countBySource = $derived(
    data.aggregations.then((agg) =>
      agg.aggregations.source.buckets.reduce(
        (acc, bucket) => ({ ...acc, [bucket.key]: bucket.doc_count }),
        {} as Record<string, number>,
      ),
    ),
  );

  function onSourceChange(value: string, checked: boolean) {
    if (value === "*") query.sources = [];
    else if (checked) query.sources.push(value);
    else query.sources = query.sources.filter((v) => v !== value);
  }
</script>

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
        checked={query.sources.includes(source.value)}
        onchange={(e) =>
          onSourceChange(e.currentTarget.id, e.currentTarget.checked)}
      />
      <label for={source.value} class="flex gap-2">
        <div>{source.label}</div>
        {#await countBySource then countBySource}
          {#if countBySource[source.value] > 0}
            <div
              class="rounded-full bg-purple-100/80 px-2.5 py-0.5 text-sm text-purple-950"
            >
              {formatNumber(countBySource[source.value])}
            </div>
          {/if}
        {/await}
      </label>
    </div>
  {/each}
</div>
