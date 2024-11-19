<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  let { data } = $props();

  const getQueryParam = () => $page.url.searchParams.get('zoek') ?? '';

  let queryInput = $state(getQueryParam());

  $effect(() => {
    queryInput = getQueryParam();
  });

  function search(e: SubmitEvent) {
    e.preventDefault();
    goto(`/dossiers/?zoek=${queryInput}`, { keepFocus: true });
  }
</script>

<form onsubmit={search}>
  <input type="search" name="zoek" bind:value={queryInput} />
  <button type="submit" class="btn btn-primary">Zoeken</button>
  {#if data.documents}
    <a href="/feeds?zoek={queryInput}" class="btn btn-primary">Nieuwe feed</a>
  {/if}
</form>

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
