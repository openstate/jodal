<script lang="ts">
    import type { Articles } from "$lib/articles";
  import ArticleBox from "../article-box.svelte";

  type Props = { articles: Articles };
  let { articles }: Props = $props();
</script>

<article class="my-30 px-6 text-stone-800">
  <h2 class="font-display mb-4 text-balance text-center text-4xl">
    Onderzoek nieuwe onderwerpen
  </h2>
  <h3 class="max-w-150 mx-auto text-center text-xl text-stone-500">
    Ontdek nieuwe onderwerpen en abonneer je op gecureerde feeds
  </h3>

  <div class="max-w-300 mx-auto my-16 grid gap-6 md:grid-cols-3">
    {#each articles as article}
      <ArticleBox {...article} />
    {/each}
  </div>
</article>
