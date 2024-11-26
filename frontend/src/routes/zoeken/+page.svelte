<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import Select from 'svelte-select';

  let { data } = $props();

  let queryInput = $state($page.url.searchParams.get('zoek') ?? '');
  let locationInput = $state([{ value: '*', label: 'Alles' }]);

  $effect(() => {
    queryInput = $page.url.searchParams.get('zoek') ?? '';
    locationInput = $page.url.searchParams
      .get('organisaties')
      ?.split(',')
      .map((id) => locationItems.find((item) => item.value === id)!) ?? [
      { value: '*', label: 'Alles' },
    ];
  });

  const locationItems = $derived(
    data.locations.hits.hits.map((hit) => ({
      value: hit._source.id,
      label: hit._source.name,
    }))
  );

  const locationIds = $derived(locationInput.map((v) => v.value).join(','));

  function search(e: SubmitEvent) {
    e.preventDefault();

    goto(`?zoek=${queryInput}&organisaties=${locationIds}`, {
      keepFocus: true,
    });
  }
</script>

<form onsubmit={search}>
  <input type="search" name="zoek" bind:value={queryInput} />

  <Select items={locationItems} multiple={true} bind:value={locationInput} />

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
