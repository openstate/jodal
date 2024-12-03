<script lang="ts">
  let { data } = $props();
</script>

<h1>Feed '{data.feed.name}'</h1>

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
