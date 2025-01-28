<script lang="ts">
  import Dialog from "$lib/components/dialog.svelte";
  import { getQueryContext } from "./state.svelte";
  import { enhance } from "$app/forms";
  import { clearCache } from "$lib/fetch";

  type Props = { open: boolean };
  let { open = $bindable() }: Props = $props();

  const query = getQueryContext();

  let name = $state("");
  let selected = $state("");
  let disabled = $derived(!name || !selected);
</script>

<Dialog bind:open>
  <form
    method="POST"
    action="/feeds"
    use:enhance={() =>
      ({ update }) => {
        clearCache("feeds");
        update();
      }}
    class="-translate-1/2 absolute left-1/2 top-1/2 w-full max-w-[min(480px,calc(100%_-_48px))] rounded-lg border border-stone-300 bg-white p-6"
  >
    <input type="hidden" name="query" value={query.term} />
    <input type="hidden" name="sources" value={query.sources.join(",")} />
    <input
      type="hidden"
      name="locations"
      value={query.organisations.join(",")}
    />

    <p class="mb-2 text-lg font-semibold">Nieuwe feed aanmaken</p>
    <p class="text-stone-700">
      Sla deze zoekopdracht op als feed om altijd op de hoogte te blijven van de
      laatste documenten.
    </p>

    <label>
      <span class="my-3 mb-2 block">Naam</span>
      <input
        name="name"
        type="text"
        bind:value={name}
        required
        placeholder="Geef je feed een naam..."
        class="w-full rounded border border-stone-300 px-3 py-2 text-stone-700 outline-0 focus:border-stone-300"
      />
    </label>
    <label>
      <span class="my-3 mb-1 block">Meldingen</span>
      <p class="mb-2 text-sm text-stone-600">
        Ontvang een mail als we nieuwe documenten gevonden hebben.
      </p>
      <select
        name="frequency"
        bind:value={selected}
        required
        class={[
          "w-full rounded border border-stone-300 px-3 py-2.5 outline-0 focus:border-stone-300",
          selected ? "text-stone-700" : "text-stone-700/50",
        ]}
      >
        <option disabled selected value="">Kies een optie...</option>
        <option value="NONE">Geen meldingen</option>
        <option value="IMMEDIATE">Directe meldingen</option>
        <option value="1d">Dagelijkse meldingen</option>
        <option value="1w">Wekelijkse meldingen</option>
      </select>
    </label>
    <!-- <div
      class="my-4 rounded-md bg-blue-100/80 px-4 py-3 text-sm text-blue-950"
    >
      Je nieuwe feed zal worden gevuld met {queryDescription}.
    </div> -->
    <div class="mt-6 flex justify-end gap-4">
      <button
        type="button"
        onclick={(e) => {
          e.preventDefault();
          open = false;
        }}
        class="cursor-pointer rounded-lg border border-stone-300 px-4 py-3 font-medium text-stone-600 disabled:opacity-50"
      >
        Annuleren
      </button>
      <button
        type="submit"
        class="cursor-pointer rounded-lg bg-black px-4 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
        {disabled}
      >
        Aanmaken
      </button>
    </div>
  </form>
</Dialog>
