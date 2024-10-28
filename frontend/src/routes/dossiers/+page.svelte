<script lang="ts">
  import { createQuery } from '$lib/query.svelte';
  import { keepPreviousData } from '@tanstack/svelte-query';
  import type { ElasticSearchResponse } from '$lib/types/elastic-search';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  let queryInput = $state($page.url.searchParams.get('q') ?? '');

  $effect(() => void goto(`/dossiers/?q=${queryInput}`, { keepFocus: true }));

  function fetchDocuments() {
    if (!queryInput) return null;

    const url =
      '//api.bron.live/documents/search?page=0&filter=|&published_to:now&sort=published:desc&limit=50';

    return fetch(url + `&query=${queryInput}`).then((r) => r.json());
  }

  const query = createQuery<ElasticSearchResponse | null>(() => ({
    queryKey: ['query', queryInput],
    queryFn: fetchDocuments,
    placeholderData: keepPreviousData,
  }));
</script>

<input type="search" bind:value={queryInput} />

{#each $query.data?.hits.hits ?? [] as hit}
  <div>
    <a href={hit._source.doc_url ?? hit._source.url}>{hit._source.title}</a>
    <p>
      <b>Locatie:</b>
      {hit._source.location_name}
      <br />
      <b>Bron:</b>
      {hit._source.source}
      <br />
      <b>Datum:</b>
      {new Date(hit._source.published).toLocaleDateString('nl', {
        dateStyle: 'long',
      })}
    </p>
    {#each hit.highlight.description as highlight}
      <p>{@html highlight}</p>
    {/each}
  </div>
{/each}
