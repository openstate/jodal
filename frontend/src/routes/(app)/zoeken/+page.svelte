<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  import Select from "svelte-select";
  import Search from "@tabler/icons-svelte/icons/search";
  import Plus from "@tabler/icons-svelte/icons/plus";

  import { allSources } from "./sources";
  import Document from "../../../lib/document.svelte";
  import { composeFilters } from "./filters";
  let { data } = $props();

  const getSelectedOrganisations = () =>
    $page.url.searchParams.get("organisaties")?.split(",") ?? [];

  const getSelectedSources = () =>
    $page.url.searchParams.get("bronnen")?.split(",") ?? [];

  let queryInput = $state($page.url.searchParams.get("zoek") ?? "");
  let selectedOrganisations = $state(getSelectedOrganisations());
  let selectedSources = $state(getSelectedSources());

  $effect(() => {
    queryInput = $page.url.searchParams.get("zoek") ?? "";
    selectedOrganisations = getSelectedOrganisations();
    selectedSources = getSelectedSources();
  });

  function search(e: SubmitEvent) {
    e.preventDefault();
    const filters = composeFilters(selectedSources, selectedOrganisations);
    const url = "?zoek=" + queryInput + filters;
    goto(url, { keepFocus: true });
  }

  function onSourceChange(value: string, checked: boolean) {
    if (value === "*" && checked)
      selectedSources = allSources.map((s) => s.value);
    else if (value === "*" && !checked) selectedSources = [];
    else if (checked) selectedSources.push(value);
    else selectedSources = selectedSources.filter((v) => v !== value);
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
      onsubmit={search}
      class="flex w-full items-center rounded-lg outline-2 outline-stone-200 focus-within:outline-stone-300 bg-white"
    >
      <input
        class="grow rounded-lg border-0 px-4 py-3 ring-0"
        type="search"
        name="zoek"
        placeholder="Zoek documenten..."
        bind:value={queryInput}
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
          checked={selectedSources.length === allSources.length}
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
            checked={selectedSources.includes(source.value)}
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
          selectedOrganisations.includes(item.value),
        )}
        on:change={(e) => {
          selectedOrganisations = e.detail.map(
            (v: { value: string }) => v.value,
          );
        }}
        on:clear={(e) => {
          selectedOrganisations = selectedOrganisations.filter(
            (v) => v !== e.detail.value,
          );
        }}
      />
    </div>
    <hr class="border-stone-200" />
  </aside>
</div>
