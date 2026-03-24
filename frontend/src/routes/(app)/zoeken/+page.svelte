<script lang="ts">
  import {
    IconBookmarkFilled,
    IconFilter,
    IconSearch,
    IconX,
  } from "@tabler/icons-svelte";

  import { type DocumentResponse } from "$lib/types/api";
  import Document from "$lib/components/document.svelte";
  import SkeletonDocument from "$lib/components/skeleton-document.svelte";
  import MakeFeed from "./make-feed.svelte";

  import SourceFilter from "./filters/source.svelte";
  import OrganisationsFilter from "./filters/organisations.svelte";
  import DateFilter from "./filters/date.svelte";

  import { createQueryState } from "./state.svelte";
  import { debounce } from "$lib/utils.svelte";
  import { fetchDocuments } from "$lib/loaders";
  import { page } from "$app/state";
  import { onMount } from "svelte";

  const { format: formatNumber } = new Intl.NumberFormat("nl-NL");

  // Reference to the DOM element that scrolls, which differs from body.
  let element = $state<HTMLElement | undefined>();
  let loadMoreButton = $state<HTMLButtonElement | undefined>();

  onMount(() => {
    element = document.getElementById("scroll") ?? undefined;
    if (!loadMoreButton || !element) return;

    const observer = new IntersectionObserver(
      (entries) =>
        entries.some((entry) => entry.isIntersecting) && onLoadMore(),
      { root: element, rootMargin: "500px 0px", threshold: 0 },
    );

    observer.observe(loadMoreButton);

    return () => observer?.disconnect();
  });

  let { data } = $props();

  let documents = $state<DocumentResponse["hits"]["hits"]>([]);
  let totalResults = $state(0);
  let pageNumber = $state(0);
  let isLoading = $state(true);

  // State object for managing the entire search query, w/ reset of documents and scroll to the top on change.
  const query = createQueryState({
    onChange: () => {
      isLoading = true;
      documents = [];
      pageNumber = 0;
      element?.scrollTo(0, 0);
    },
  });

  // Mobile-only visibility state.
  let filtersOpen = $state(false);
  let newFeedsOpen = $state(false);

  // Effect to update `documents` with awaited `data.documents`, on load and when URL changes.
  $effect(() => {
    const loadDocuments = async () => {
      isLoading = true;
      try {
        const response = await data.documents;
        pageNumber = 0;
        totalResults = response.hits.total.value;
        documents = response.hits.hits;
      } finally {
        isLoading = false;
      }
    };

    loadDocuments();
  });

  const hasMoreResults = $derived(documents.length < totalResults);

  // Function to load more documents when the user scrolls to the bottom.
  const onLoadMore = async () => {
    if (isLoading) return;
    if (!hasMoreResults) return;

    isLoading = true;
    try {
      const nextPage = pageNumber + 1;
      const newDocuments = await fetchDocuments({
        url: page.url,
        locations: data.locations,
        pageNumber: nextPage,
        fetch,
      });

      pageNumber = nextPage;
      documents = documents.concat(newDocuments.hits.hits);
    } finally {
      isLoading = false;
    }
  };

  // Debounced function to set the query term on input bind.
  const setQueryTerm = debounce((v: string) => {
    if (v !== query.term) query.term = v;
  }, 500);
</script>

<svelte:head>
  <title>Zoeken &ndash; Bron</title>
</svelte:head>

<MakeFeed bind:open={newFeedsOpen} />

<div class="mx-auto grid max-w-300 gap-10 px-6 md:grid-cols-[1fr_20rem]">
  <div>
    <form
      onsubmit={(e) => {
        e.preventDefault();
        query.term = new FormData(e.currentTarget).get("zoek") as string;
      }}
      class="sticky -top-4 z-10 border-b border-stone-300 bg-stone-50 pt-8 pb-4 max-md:-m-6 max-md:-mb-2 max-md:w-screen max-md:px-6 md:top-0"
    >
      <div
        class="flex w-full items-center rounded-lg border border-stone-300 bg-white outline-0 transition focus-within:border-stone-300"
      >
        <!-- svelte-ignore a11y_autofocus -- search is legitimate use of autofocus -->
        <input
          autofocus={true}
          class="grow rounded-lg border-0 px-4 py-3 ring-0 outline-0"
          type="search"
          name="zoek"
          placeholder="Zoek documenten..."
          value={query.term}
          oninput={(e) => setQueryTerm(e.currentTarget.value)}
        />
        <button type="submit" class="mx-2 cursor-pointer p-2 text-stone-700">
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
      <div class="flex flex-wrap justify-between gap-2">
        {#await data.documents}
          <div
            class="my-1 h-4 w-32 animate-pulse rounded-lg bg-stone-200 font-medium"
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
        <a
          href="/over"
          class="text-stone-600 underline transition hover:text-stone-800"
        >
          Hoe werkt Bron?
        </a>
      </div>

      {#each documents as document (document._id)}
        <Document {document} />
      {/each}

      {#if isLoading}
        {#each { length: documents.length === 0 ? 20 : 3 }}
          <SkeletonDocument />
        {/each}
      {/if}

      <div class={["mb-10", !hasMoreResults && "hidden"]}>
        <button
          bind:this={loadMoreButton}
          class="cursor-pointer rounded-lg border border-stone-300 bg-white px-4 py-2 font-medium text-stone-800 transition hover:bg-stone-100 disabled:cursor-auto disabled:opacity-50"
          onclick={onLoadMore}
          disabled={isLoading || !hasMoreResults}
          type="button"
        >
          Meer resultaten tonen
        </button>
      </div>
    </div>
  </div>
  <aside
    class={[
      "relative transition max-md:fixed max-md:inset-0 max-md:top-16 max-md:z-20 md:w-80 md:shrink-0 md:pt-8",
      filtersOpen ? "max-md:bg-black/50" : "max-md:pointer-events-none",
    ]}
  >
    <div
      class={[
        "pointer-events-auto h-full space-y-6 overflow-x-visible overflow-y-scroll bg-stone-50 transition duration-300 max-md:ml-auto max-md:max-w-[90vw] max-md:border-l max-md:border-stone-300 max-md:p-8 md:fixed md:w-80",
        !filtersOpen && "max-md:translate-x-full",
      ]}
    >
      <button
        class="absolute top-8 right-8 md:hidden"
        onclick={() => (filtersOpen = false)}
      >
        <IconX class="text-stone-800" />
      </button>

      <button
        class="mb-4.5 flex cursor-pointer items-center gap-2 rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:cursor-auto disabled:opacity-20 max-md:hidden"
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
