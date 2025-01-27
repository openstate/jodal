<script lang="ts">
  import ArticleBox from "$lib/components/article-box.svelte";

  let { data } = $props();
</script>

<svelte:head>
  <title>Gids &ndash; Bron</title>
</svelte:head>

<div class="lg:max-w-300 px-6 py-12 lg:mx-auto">
  <h1 class="font-display mb-6 text-2xl font-medium">Jouw gids</h1>
  <p class="mb-10 text-lg text-stone-700">
    Met onze gidsartikelen helpen we jou op weg om diepgravend onderzoek in jouw
    regio te doen.
  </p>
  <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
    {#each data.articles as article}
      <ArticleBox {...article} />
    {/each}
  </div>
</div>
