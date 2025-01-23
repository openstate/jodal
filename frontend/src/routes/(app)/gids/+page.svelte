<script lang="ts">
  import ArticleBox from "$lib/components/article-box.svelte";

  let { data } = $props();
</script>

<div class="lg:max-w-300 px-6 py-8 lg:mx-auto">
  <h1 class="mb-6 text-2xl font-display font-medium">Jouw gids</h1>
  <p class="text-stone-700 text-lg mb-10">Met onze gidsartikelen helpen we jou op weg om diepgravend onderzoek in jouw regio te doen.</p>
  <div class="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
    {#each data.articles as article}
      <ArticleBox {...article} />
    {/each}
  </div>
</div>
