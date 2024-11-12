<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  let queryInput = $state($page.url.searchParams.get('q') ?? '');

  $effect(() => void goto(`/dossiers/?q=${queryInput}`, { keepFocus: true }));

  let { data } = $props();
</script>

<input type="search" bind:value={queryInput} />

{#each data.documents?.hits.hits ?? [] as hit}
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
