<script lang="ts">
  import Document from "$lib/components/document.svelte";
  import SkeletonDocument from "$lib/components/skeleton-document.svelte";

  let { data } = $props();
</script>

<div class="space-y-4">
  <h1 class="text-xl font-semibold">Feed '{data.feed.name}'</h1>
  {#await data.documents}
    {#each { length: 10 } as _}
      <SkeletonDocument />
    {/each}
  {:then documents}
    {#each documents?.hits.hits ?? [] as document}
      <Document {document} />
    {/each}
  {/await}
</div>
