<script lang="ts">
  import { dev } from "$app/environment";
  import Document from "$lib/components/document.svelte";
  import SkeletonDocument from "$lib/components/skeleton-document.svelte";

  let { data } = $props();
  if (dev) $inspect(data.documents).with(async (_, d) => console.log(await d));

  const capitalizeFirst = (str: string) => str.charAt(0).toUpperCase() + str.slice(1);
</script>

<svelte:head>
  <title>{capitalizeFirst(data.feed.name)} &ndash; Bron</title>
</svelte:head>

<div class="lg:max-w-300 space-y-4 px-4 py-8 lg:mx-auto">
  <h1 class="text-xl font-semibold">Feed '{data.feed.name}'</h1>
  {#await data.documents}
    {#each { length: 20 } as _}
      <SkeletonDocument />
    {/each}
  {:then documents}
    {#each documents?.hits.hits ?? [] as document}
      <Document {document} />
    {/each}
  {/await}
</div>
