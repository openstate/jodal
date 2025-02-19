<script lang="ts">
  import { getQueryContext } from "../state.svelte";
  import type { PageData } from "../$types";
  import Fuse from "fuse.js";
  import { getLocationItems } from "$lib/loaders";

  let { data }: { data: PageData } = $props();

  const query = getQueryContext();

  let showMore = $state(false);
  let search = $state("");
  let noSearch = $derived(search === "");

  const items = $derived(getLocationItems(data.locations));

  const fuse = $derived(new Fuse(items, { keys: ["label"] }));

  let filteredItems = $derived(
    search === "" ? items : fuse.search(search).map((r) => r.item),
  );

  let selectedItems = $derived(
    items.filter((i) => query.organisations.includes(i.value)),
  );

  let shownItems = $derived(
    filteredItems
      .slice(0, showMore && !noSearch ? 14 : 4)
      .concat(
        noSearch
          ? selectedItems.filter(
              (i) => i.value !== "*" && !i.value.startsWith("type:"),
            )
          : [],
      ),
  );

  $effect(() => {
    if (noSearch) showMore = false;
  });

  function onOrganisationChange(value: string, checked: boolean) {
    if (value === "*") query.organisations = [];
    else if (checked) query.organisations.push(value);
    else query.organisations = query.organisations.filter((v) => v !== value);
  }
</script>

<div class="space-y-1">
  <h2 class="mb-3 font-bold">Organisaties</h2>
  <input
    type="text"
    bind:value={search}
    placeholder="Zoek organisaties..."
    class="mb-4 w-full rounded-lg border border-stone-300 bg-white px-4 py-3 outline-0 transition focus-within:border-stone-300"
  />
  {#each shownItems as item}
    <div class="flex items-center gap-2">
      <input
        type="checkbox"
        id={item.value}
        checked={query.organisations.includes(item.value)}
        onchange={(e) =>
          onOrganisationChange(e.currentTarget.id, e.currentTarget.checked)}
      />
      <label for={item.value}>
        {item.label}
      </label>
    </div>
  {/each}
  {#if filteredItems.length > 4 && !noSearch}
    <button
      class="cursor-pointer font-medium text-blue-700"
      onclick={() => (showMore = !showMore)}
    >
      {#if showMore}Minder...{:else}Meer...{/if}
    </button>
  {/if}
</div>
