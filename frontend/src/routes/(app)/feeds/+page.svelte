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

<div class="lg:max-w-300 px-6 py-8 lg:mx-auto">
  <h1 class="font-display mb-6 text-2xl font-medium">Jouw feeds</h1>
  <p class="mb-10 text-lg text-stone-700">
    Met feeds blijf je altijd op de hoogte van de nieuwste overheidsdocumenten
    in jouw onderzoeksgebied.
  </p>

  <div class="rounded-lg border border-stone-300 bg-white px-6 py-5">
    {#if data.feeds.length > 0}
      <table class="w-full table-fixed">
        <thead>
          <tr>
            <th class="px-2 py-4 text-left font-semibold">Naam</th>
            <th class="px-2 py-4 text-left font-semibold max-md:hidden"
              >Zoekterm</th
            >
            <th class="px-2 py-4 text-left font-semibold max-xl:hidden"
              >Filters</th
            >
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
                class="border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0"
              >
                {feed.name}
              </td>
              <td
                class="border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0 max-md:hidden"
              >
                {feed.query}
              </td>
              <td
                class="border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0 max-xl:hidden"
              >
                <span class={[filterCount === 0 && "text-stone-500"]}>
                  {formatFilterCount(filterCount)}
                </span>
              </td>
              <td
                class="border-y border-stone-300 px-2 py-4 group-last-of-type:border-b-0 max-sm:hidden"
              >
                {#await feed.match then match}
                  <span class={[!match.hits.hits.at(-1) && "text-stone-500"]}>
                    {formatDuration(match.hits.hits.at(-1)?._source.processed)}
                  </span>
                {/await}
              </td>
              <td
                class="border-y border-stone-300 px-2 py-4 pr-5 font-semibold text-blue-700 group-last-of-type:border-b-0"
              >
                <a
                  href="/feeds/{feed.public_id}"
                  class="ml-auto flex w-fit cursor-pointer items-center gap-1 rounded-lg bg-blue-100 px-3 py-1.5 pr-4 transition hover:bg-blue-100"
                >
                  <IconArrowNarrowRight />
                  Bekijken
                </a>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    {:else}
      <p class="text-lg text-stone-800">
        Je hebt nog geen feeds aangemaakt. Doorzoek documenten, pas filters toe,
        en klik dan op 'Bewaar zoekopdracht'.
      </p>
      <a
        href="/zoeken"
        class="mt-4 block w-fit cursor-pointer rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:cursor-auto disabled:opacity-20"
        >Zoeken</a
      >
    {/if}
  </div>
</div>
