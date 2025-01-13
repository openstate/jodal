<script lang="ts">
  import { IconArrowNarrowRight } from "@tabler/icons-svelte";

  let { data } = $props();

  let pluralize = (n: number, singular: string, plural: string) =>
    n + " " + (n === 1 ? singular : plural);

  function formatDuration(date?: string) {
    if (!date) return "Nog geen matches";
    const diff = new Date().getTime() - new Date(date).getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    if (days === 0) return "Vandaag";
    if (days === 1) return "Gisteren";
    if (days <= 30) return pluralize(days, "dag geleden", "dagen geleden");
    return new Date(date).toLocaleDateString("nl", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  }

  function formatFilterCount(count: number) {
    return count === 0 ? "Geen filters" : pluralize(count, "filter", "filters");
  }
</script>

<h1 class="mb-6 text-2xl font-bold">Jouw feeds</h1>

<div class="rounded-lg border-2 border-stone-200 bg-white px-6 py-5">
  <table class="w-full table-fixed">
    <thead>
      <tr>
        <th class="px-2 py-4 text-left font-semibold">Naam</th>
        <th class="px-2 py-4 text-left font-semibold max-md:hidden">Zoekterm</th
        >
        <th class="px-2 py-4 text-left font-semibold max-xl:hidden">Filters</th>
        <th class="px-2 py-4 text-left font-semibold max-sm:hidden"
          >Laatste match</th
        >
        <th class="px-2 py-4 text-left font-semibold"></th>
      </tr>
    </thead>
    <tbody>
      {#each data.feeds ?? [] as feed}
        {@const filterCount = feed.sources.length + feed.locations.length}
        <tr class="group">
          <td
            class="border-y border-stone-200 px-2 py-4 group-last-of-type:border-b-0"
          >
            {feed.name}
          </td>
          <td
            class="border-y border-stone-200 px-2 py-4 group-last-of-type:border-b-0 max-md:hidden"
          >
            {feed.query}
          </td>
          <td
            class="border-y border-stone-200 px-2 py-4 group-last-of-type:border-b-0 max-xl:hidden"
          >
            <span class={[filterCount === 0 && "text-stone-500"]}>
              {formatFilterCount(filterCount)}
            </span>
          </td>
          <td
            class="border-y border-stone-200 px-2 py-4 group-last-of-type:border-b-0 max-sm:hidden"
          >
            {#await feed.match then match}
              <span class={[!match.hits.hits.at(-1) && "text-stone-500"]}>
                {formatDuration(match.hits.hits.at(-1)?._source.processed)}
              </span>
            {/await}
          </td>
          <td
            class="border-y border-stone-200 px-2 py-4 pr-5 font-semibold text-purple-700 group-last-of-type:border-b-0"
          >
            <a
              href="/feeds/{feed.public_id}"
              class="ml-auto flex w-fit cursor-pointer items-center gap-1 rounded-lg bg-purple-100 px-3 py-1.5 pr-4 transition hover:bg-purple-200"
            >
              <IconArrowNarrowRight />
              Bekijken
            </a>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
