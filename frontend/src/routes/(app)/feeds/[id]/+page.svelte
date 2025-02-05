<script lang="ts">
  import { dev } from "$app/environment";
  import { enhance } from "$app/forms";
  import { page } from "$app/state";
  import Document from "$lib/components/document.svelte";
  import SkeletonDocument from "$lib/components/skeleton-document.svelte";
  import { clearCache } from "$lib/fetch.js";
  import { allSources } from "$lib/sources";
  import { IconTrash } from "@tabler/icons-svelte";

  let { data } = $props();
  if (dev) $inspect(data.documents).with(async (_, d) => console.log(await d));

  const capitalizeFirst = (str: string) =>
    str.charAt(0).toUpperCase() + str.slice(1);

  let pluralize = (n: number, singular: string, plural: string) =>
    n + " " + (n === 1 ? singular : plural);

  let queryDescription = $derived.by(() => {
    let documents =
      data.feed.query === ""
        ? "alle documenten"
        : `documenten met de term "${data.feed.query}"`;

    let sources = [0, allSources.length].includes(data.feed.sources.length)
      ? "alle bronnen"
      : pluralize(data.feed.sources.length, "bron", "bronnen");

    let organisations =
      data.feed.locations.length === 0
        ? "alle organisaties"
        : pluralize(data.feed.locations.length, "organisatie", "organisaties");

    let frequency =
      data.feed.binoas_frequency === null
        ? "geen"
        : data.feed.binoas_frequency === ""
          ? "direct een"
          : data.feed.binoas_frequency == "1d"
            ? "dagelijks een"
            : "wekelijks een";

    return `In deze feed verschijnen ${documents} uit ${sources} van ${organisations}. Je ontvangt ${frequency} e-mail als er nieuwe documenten gevonden worden.`;
  });
</script>

<svelte:head>
  <title>{capitalizeFirst(data.feed.name)} &ndash; Bron</title>
</svelte:head>

<div class="max-w-300 mx-auto w-full px-6 py-12">
  <div class="max-w-200 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="font-display text-2xl font-medium">
        Feed &mdash; {capitalizeFirst(data.feed.name)}
      </h1>
      <form
        action="?/delete"
        method="post"
        use:enhance={() =>
          ({ update }) => {
            clearCache("feeds");
            clearCache(`feed:${page.params.id}`);
            update();
          }}
      >
        <button
          class="flex cursor-pointer items-center justify-center gap-2 rounded-lg border border-stone-300 bg-white px-3 py-1.5 font-medium text-stone-700 transition hover:bg-stone-100 max-sm:aspect-square sm:px-4"
          type="submit"
        >
          <IconTrash class="size-4.5 sm:-ml-1" />
          <span class="max-sm:hidden">Verwijderen</span>
        </button>
      </form>
    </div>
    <p class="mb-10 text-lg text-stone-700">
      {queryDescription}
    </p>
    {#await data.documents}
      {#each { length: 20 } as _}
        <SkeletonDocument />
      {/each}
    {:then documents}
      {#each documents?.hits.hits ?? [] as document}
        <Document {document} datePriority={["processed", "published"]} />
      {:else}
        <p>Geen documenten gevonden voor deze feed.</p>
      {/each}
    {/await}
  </div>
</div>
