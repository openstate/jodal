<script lang="ts">
  import { getQueryContext } from "../state.svelte";

  const query = getQueryContext();
</script>

<div class="space-y-1">
  <h2 class="mb-3 font-bold">Datum</h2>
  <p class="my-2 text-stone-700">Startdatum</p>
  <input
    type="date"
    bind:value={query.dateFrom}
    class={[
      "w-full rounded-lg border-2 border-stone-200 bg-white px-4 py-3 outline-0 transition focus-within:border-stone-300",
      query.dateFrom ? "text-stone-800" : "text-stone-500",
    ]}
  />
  <p class="my-2 text-stone-700">Einddatum</p>
  <input
    type="date"
    bind:value={query.dateTo}
    class={[
      "w-full rounded-lg border-2 border-stone-200 bg-white px-4 py-3 outline-0 transition focus-within:border-stone-300",
      query.dateTo ? "text-stone-800" : "text-stone-500",
    ]}
  />
</div>
