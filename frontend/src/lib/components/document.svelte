<script lang="ts">
  import type { DocumentResponse, DocumentSource } from "$lib/types/api";

  import Buildings from "@tabler/icons-svelte/icons/buildings";
  import Calendar from "@tabler/icons-svelte/icons/calendar";
  import Database from "@tabler/icons-svelte/icons/database";

  import { allSources } from "$lib/sources";
  import { IconExternalLink } from "@tabler/icons-svelte";

  type Props = {
    document: DocumentResponse["hits"]["hits"][number];
    datePriority?: Array<"processed" | "modified" | "created" | "published">;
  };

  let { document, datePriority = ["published", "processed"] }: Props = $props();

  const documentUrl = $derived(
    document._source.doc_url ?? document._source.url,
  );

  const date = $derived.by(() => {
    const dates = datePriority.map((key) => new Date(document._source[key]));
    return dates.find((date) => date.toString() !== "Invalid Date") ?? null;
  });

  const formattedDate = $derived.by(() => {
    if (!date) return "Onbekende datum";
    return date.toLocaleDateString("nl", { dateStyle: "long" });
  });
</script>

<div class="block rounded-lg border border-stone-300 bg-white p-4">
  <div class="mb-2 flex items-center justify-between gap-1">
    <a target="_blank" href={documentUrl} class="font-semibold hover:underline">
      {document._source.title}
    </a>
    <a target="_blank" href={documentUrl}>
      <IconExternalLink class="inline size-4 text-stone-600" />
    </a>
  </div>
  {#if document.highlight?.description && document.highlight.description.length > 0}
    <p class="my-2 line-clamp-5 text-stone-800 [word-break:break-word]">
      …{@html document.highlight.description
        ?.join(" … ")
        .replace(/<(?!\/?em\b)[^>]+>/g, "")
        .replace(/\.$/g, "")}…
    </p>
  {/if}
  <div class="flex flex-wrap items-center gap-2 text-sm">
    <div
      class="flex items-center gap-2 rounded-md bg-blue-100/80 px-2 py-0.5 font-medium text-blue-900"
    >
      <Calendar class="w-4" />
      {formattedDate}
    </div>
    <div
      class="flex items-center gap-2 rounded-md bg-blue-100/80 px-2 py-0.5 font-medium text-blue-900"
    >
      <Buildings class="w-4" />
      {document._source.location_name}
    </div>
    <div
      class="flex items-center gap-2 rounded-md bg-blue-100/80 px-2 py-0.5 font-medium text-blue-900"
    >
      <Database class="w-4" />
      {allSources.find((s) => s.value === document._source.source)?.label}
    </div>
  </div>
</div>

<style>
  p :global(em) {
    font-style: normal;
    color: var(--color-blue-800);
    font-weight: 500;
    text-decoration: underline;
  }
</style>
