<script lang="ts">
  import Document from "$lib/document.svelte";

  let { data } = $props();
</script>

<div class="space-y-4">
  <h1 class="text-xl font-semibold">Feed '{data.feed.name}'</h1>
  {#each data.documents?.hits.hits ?? [] as document}
    <Document {document} />
  {/each}
</div>
