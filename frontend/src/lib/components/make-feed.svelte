<script lang="ts">
  import Plus from "@tabler/icons-svelte/icons/plus";
  import Dialog from "$lib/components/dialog.svelte";
  import type { Query } from "../../routes/(app)/zoeken/state.svelte";
  import { allSources } from "../../routes/(app)/zoeken/sources";

  type Props = { query: Query };
  let { query }: Props = $props();

  let open = $state(false);
  let selected = $state("");

  let pluralize = (n: number, singular: string, plural: string) =>
    n + " " + (n === 1 ? singular : plural);

  let queryDescription = $derived.by(() => {
    let sources = [0, allSources.length].includes(query.sources.length)
      ? "alle bronnen"
      : pluralize(query.sources.length, "bron", "bronnen");

    let organisations =
      query.organisations.length === 0
        ? "alle organisaties"
        : pluralize(query.organisations.length, "organisatie", "organisaties");

    return `met de term "${query.term}" uit ${sources} van ${organisations}`;
  });
</script>

<button
  class="flex cursor-pointer items-center gap-4 rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:cursor-auto disabled:opacity-20"
  disabled={!query.term}
  onclick={() => (open = true)}
>
  <Plus class="w-5" />
  Sla zoekopdracht op
</button>

<Dialog bind:open>
  <div
    class="-translate-1/2 absolute left-1/2 top-1/2 w-full max-w-[min(480px,calc(100%_-_48px))] rounded-lg border-2 border-stone-200 bg-white p-6"
  >
    <p class="mb-2 text-lg font-semibold">Nieuwe feed aanmaken</p>
    <p class="text-stone-700">
      Sla deze zoekopdracht op als feed om altijd op de hoogte te blijven van de
      laatste documenten.
    </p>

    <label>
      <span class="my-3 mb-2 block">Naam</span>
      <input
        type="text"
        placeholder="Geef je feed een herkenbare naam..."
        class="w-full rounded border-2 border-stone-200 px-3 py-2 text-stone-700 outline-0 focus:border-stone-300"
      />
    </label>
    <label>
      <span class="my-3 mb-1 block">Meldingen</span>
      <p class="text-sm text-stone-600 mb-2">Ontvang een mail als we nieuwe documenten gevonden hebben.</p>
      <select
        bind:value={selected}
        class={[
          "w-full rounded border-2 border-stone-200 px-3 py-2.5 outline-0 focus:border-stone-300",
          selected ? "text-stone-700" : "text-stone-700/50",
        ]}
      >
        <option disabled selected value="">Kies een optie...</option>
        <option value="none">Geen meldingen</option>
        <option value="immediate">Directe meldingen</option>
        <option value="hourly">Uurlijkse meldingen</option>
        <option value="daily">Dagelijkse meldingen</option>
        <option value="weekly">Wekelijkse meldingen</option>
      </select>
    </label>
    <div class="my-4 rounded-md bg-purple-100/80 px-4 py-3 text-purple-950">
      <p class="mb-1 flex items-center gap-2 font-medium">Jouw zoekopdracht</p>
      <p class="text-purple-950/80">
        Je nieuwe feed zal worden gevuld met documenten {queryDescription}.
      </p>
    </div>
    <div class="flex justify-end gap-4">
      <button
        onclick={() => (open = false)}
        class="cursor-pointer rounded-lg border-2 border-stone-200 px-4 py-3 font-medium text-stone-600 disabled:opacity-50"
      >
        Annuleren
      </button>
      <button
        class="cursor-pointer rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:opacity-50"
      >
        Aanmaken
      </button>
    </div>
  </div>
</Dialog>
