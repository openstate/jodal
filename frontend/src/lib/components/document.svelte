<script lang="ts">
  import type { DocumentResponse } from "$lib/types/api";

  import Buildings from "@tabler/icons-svelte/icons/buildings";
  import Calendar from "@tabler/icons-svelte/icons/calendar";
  import Database from "@tabler/icons-svelte/icons/database";

  import { allSources } from "../../routes/(app)/zoeken/sources";

  type Props = { document: DocumentResponse["hits"]["hits"][number] };

  let { document }: Props = $props();

  function getDocumentDate() {
    const dateKeys = ["processed", "published", "created"] as const;
    const dates = dateKeys.map((key) => new Date(document._source[key]));
    return dates.find((date) => date.toString() !== "Invalid Date") ?? null;
  }

  function formatDate(date: Date | null) {
    if (!date) return "Onbekende datum";
    return date.toLocaleDateString("nl", { dateStyle: "long" });
  }

  const date = $derived(getDocumentDate());
</script>

<a
  target="_blank"
  href={document._source.doc_url ?? document._source.url}
  class="block rounded-lg border-2 border-stone-200 bg-white p-4"
>
  <h2 class="mb-2 font-semibold">{document._source.title}</h2>
  {#if document.highlight?.description && document.highlight.description.length > 0}
    <p class="my-2 line-clamp-3 text-stone-800">
      …{@html document.highlight.description
        ?.join(" … ")
        .replace(/<(?!\/?em\b)[^>]+>/g, "")
        .replace(/\.$/g, "")}…
    </p>
  {/if}
  <div class="flex flex-wrap items-center gap-2 text-sm">
    <div
      class="flex items-center gap-2 rounded-md bg-purple-100/80 px-2 py-0.5 text-purple-950"
    >
      <Calendar class="w-4" />
      {formatDate(date)}
    </div>
    <div
      class="flex items-center gap-2 rounded-md bg-purple-100/80 px-2 py-0.5 text-purple-950"
    >
      <Buildings class="ml-2 w-4" />
      {document._source.location_name}
    </div>
    <div
      class="flex items-center gap-2 rounded-md bg-purple-100/80 px-2 py-0.5 text-purple-950"
    >
      <Database class="ml-2 w-4" />
      {allSources.find((s) => s.value === document._source.source)?.label}
    </div>
  </div>
</a>

<style>
  p :global(em) {
    font-style: normal;
    color: var(--color-purple-800);
    font-weight: 500;
    text-decoration: underline;
  }
</style>
