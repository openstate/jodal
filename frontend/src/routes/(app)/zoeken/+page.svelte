<script lang="ts">
  import {
    IconBookmarkFilled,
    IconFilter,
    IconSearch,
    IconX,
  } from "@tabler/icons-svelte";

  import InfiniteScroll from "svelte-infinite-scroll";

  import { type DocumentResponse } from "$lib/types/api";
  import Document from "$lib/components/document.svelte";
  import SkeletonDocument from "$lib/components/skeleton-document.svelte";
  import MakeFeed from "./make-feed.svelte";

  import SourceFilter from "./filters/source.svelte";
  import OrganisationsFilter from "./filters/organisations.svelte";
  import DateFilter from "./filters/date.svelte";

  import { createQueryState } from "./state.svelte";
  import { debounce } from "$lib/utils";
  import { browser } from "$app/environment";
  import { fetchDocuments } from "$lib/loaders";
  import { page } from "$app/state";

  const { format: formatNumber } = new Intl.NumberFormat("nl-NL");

  // Reference to the DOM element that scrolls, which differs from body.
  const element = (browser && document?.getElementById("scroll")) || undefined;

  let { data } = $props();

  let documents = $state<DocumentResponse["hits"]["hits"]>([]);
  let pageNumber = $state(0);
  let isLoading = $state(true);

  // State object for managing the entire search query, w/ reset of documents and scroll to the top on change.
  const query = createQueryState({
    onChange: () => {
      isLoading = true;
      documents = [];
      element?.scrollTo(0, 0);
    },
  });

  // Mobile-only visibility state.
  let filtersOpen = $state(false);
  let newFeedsOpen = $state(false);

  // Wraps an async function to set `isLoading` before and after execution.
  const wrapLoading =
    <T,>(fn: () => Promise<T>) =>
    () => {
      isLoading = true;
      fn().finally(() => (isLoading = false));
    };

  // Effect to update `documents` with awaited `data.documents`, on load and when URL changes.
  $effect(() => {
    let documentPromise = data.documents.then((d) => d.hits.hits);
    const loadDocuments = wrapLoading(async () => {
      documents = await documentPromise;
    });
    loadDocuments();
  });

  // Function to load more documents when the user scrolls to the bottom.
  const onLoadMore = wrapLoading(async () => {
    const newDocuments = await fetchDocuments({
      url: page.url,
      locations: data.locations,
      pageNumber: ++pageNumber,
      fetch,
    });

    documents = documents.concat(newDocuments.hits.hits);
  });

  // Debounced function to set the query term on input bind.
  const setQueryTerm = debounce((v) => {
    if (v !== query.term) query.term = v;
  }, 500);

  $inspect(isLoading);
</script>

<MakeFeed bind:open={newFeedsOpen} />

<div class="max-w-300 mx-auto grid gap-10 px-6 md:grid-cols-[1fr_20rem]">
  <div class="grow">
    <form
      onsubmit={(e) => {
        e.preventDefault();
        query.term = new FormData(e.currentTarget).get("zoek") as string;
      }}
      class="sticky -top-4 z-10 border-b border-stone-300 bg-stone-50 pb-4 pt-8 max-md:-m-4 max-md:w-screen max-md:px-4 md:top-0"
    >
      <div
        class="flex w-full items-center rounded-lg border border-stone-300 bg-white outline-0 transition focus-within:border-stone-300"
      >
        <!-- svelte-ignore a11y_autofocus -- search is legitimate use of autofocus -->
        <input
          autofocus={true}
          class="grow rounded-lg border-0 px-4 py-3 outline-0 ring-0"
          type="search"
          name="zoek"
          placeholder="Zoek documenten..."
          value={query.term}
          oninput={(e) => setQueryTerm(e.currentTarget.value)}
        />
        <button type="submit" class="mx-2 cursor-pointer p-2">
          <IconSearch />
        </button>
      </div>

      <div class="mt-2 flex justify-between gap-3 md:hidden">
        <button
          class="flex grow items-center justify-center gap-1.5 rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-stone-800"
          onclick={() => (filtersOpen = !filtersOpen)}
          type="button"
        >
          <IconFilter class="-ml-1 size-4" />
          Filter
        </button>
        <button
          class="flex grow items-center justify-center gap-1.5 rounded-lg bg-black px-2.5 py-1.5 font-medium text-white"
          onclick={() => (newFeedsOpen = true)}
          type="button"
        >
          <IconBookmarkFilled class="-ml-1 size-4" />
          Bewaar
        </button>
      </div>
    </form>

    <div class="mt-10 space-y-4 md:mt-6">
      {#await data.documents}
        <div
          class="my-5 h-4 w-36 animate-pulse rounded-lg bg-stone-200 font-medium"
        ></div>
      {:then { hits }}
        <p>
          {#if hits.total.value === 0}
            Geen resultaten
          {:else}
            {formatNumber(
              hits.total.value,
            )}{#if hits.total.relation === "gte"}+{/if}
            {#if hits.total.value === 1}resultaat{:else}resultaten{/if}
          {/if}
        </p>
      {/await}

      {#each documents as document}
        <Document {document} />
      {/each}

      {#if isLoading}
        {#each { length: documents.length === 0 ? 20 : 3 }}
          <SkeletonDocument />
        {/each}
      {/if}

      <InfiniteScroll
        threshold={500}
        on:loadMore={onLoadMore}
        elementScroll={element}
      />
    </div>
  </div>
  <aside
    class={[
      "relative pt-8 transition max-md:fixed max-md:inset-0 max-md:top-16 max-md:z-20 md:w-80 md:shrink-0",
      filtersOpen ? "max-md:bg-black/50" : "max-md:pointer-events-none",
    ]}
  >
    <div
      class={[
        "max-md:max-w-90 pointer-events-auto h-full space-y-6 overflow-x-visible overflow-y-scroll bg-stone-50 transition duration-300 max-md:ml-auto max-md:border-l max-md:border-stone-300 max-md:p-8 md:fixed md:w-80",
        !filtersOpen && "max-md:translate-x-full",
      ]}
    >
      <button
        class="absolute right-8 top-8 md:hidden"
        onclick={() => (filtersOpen = false)}
      >
        <IconX class="text-stone-800" />
      </button>

      <button
        class="flex cursor-pointer items-center gap-2 rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:cursor-auto disabled:opacity-20 max-md:hidden"
        onclick={() => (newFeedsOpen = true)}
      >
        <IconBookmarkFilled class="size-5" />
        Bewaar zoekopdracht
      </button>

      <hr class="border-stone-300 max-md:hidden" />

      <SourceFilter {data} />

      <hr class="border-stone-300" />

      <OrganisationsFilter {data} />

      <hr class="border-stone-300" />

      <DateFilter />

      <hr class="border-stone-300" />

      <button
        class="flex w-full cursor-pointer items-center justify-center gap-2 rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:cursor-auto disabled:opacity-20 md:hidden"
        onclick={() => (filtersOpen = false)}
      >
        Filters toepassen
      </button>
    </div>
  </aside>
</div>
