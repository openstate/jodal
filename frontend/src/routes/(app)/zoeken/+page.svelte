<script lang="ts">
  import Select from "svelte-select";
  import Search from "@tabler/icons-svelte/icons/search";
  import Plus from "@tabler/icons-svelte/icons/plus";

  import { allSources } from "./sources";
  import Document from "../../../lib/document.svelte";
  import { createQueryState } from "./state.svelte";
  import { debounce } from "$lib/utils";

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

  const organisationItems = $derived(
    data.locations.hits.hits.map((hit) => ({
      value: hit._source.id,
      label: hit._source.name,
    })),
  );
</script>

<div class="grid grid-cols-[2fr_1fr] gap-16">
  <div class="space-y-4">
    <form
      onsubmit={(e) => (e.preventDefault(), (query.term = searchInput))}
      class="flex w-full items-center rounded-lg bg-white outline-2 outline-stone-200 focus-within:outline-stone-300"
    >
      <input
        class="grow rounded-lg border-0 px-4 py-3 ring-0"
        type="search"
        name="zoek"
        placeholder="Zoek documenten..."
        bind:value={searchInput}
      />
      <button type="submit" class="mx-2 cursor-pointer p-2">
        <Search />
      </button>
    </form>

    <p class="font-medium">
      {#if !data.documents}
        Zoek naar bijvoorbeeld 'fietsers' om documenten te vinden.
      {:else if data.documents.hits.total.value === 0}
        Geen resultaten
      {:else}
        {data.documents.hits.total.value}
        {#if data.documents.hits.total.value === 1}resultaat{:else}resultaten{/if}
      {/if}
    </p>

    {#each data.documents?.hits.hits ?? [] as document}
      <Document {document} />
    {/each}
  </div>
  <aside class="space-y-6">
    <button
      class="flex cursor-pointer items-center gap-4 rounded-lg bg-black px-4 py-3 font-semibold text-white"
    >
      <Plus class="w-5" />
      Sla zoekopdracht op
    </button>
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
          <label for={source.value}>{source.label}</label>
        </div>
      {/each}
    </div>
    <hr class="border-stone-200" />
    <div class="space-y-1">
      <h2 class="mb-3 font-bold">Organisaties</h2>
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
    </div>
    <hr class="border-stone-200" />
  </aside>
</div>
