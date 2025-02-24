<script lang="ts">
  import type { AggregationsQuarterlyDocuments } from "$lib/types/api";
  import { BarChart, Tooltip } from "layerchart";

  const { format: formatNumber } = new Intl.NumberFormat("nl-NL");

  let { data }: { data: AggregationsQuarterlyDocuments } = $props();

  const quarters = $derived.by(() => {
    const now = new Date();
    let year = now.getFullYear();
    let quarter = Math.floor(now.getMonth() / 3) + 1;

    return Array.from({ length: 41 }, () => {
      const result = `Q${quarter} ${year}`;
      quarter = quarter === 1 ? 4 : quarter - 1;
      if (quarter === 4) year--;
      return result;
    }).toReversed();
  });

  const chart = $derived.by(() => {
    return quarters.map((key) => {
      const doc_count =
        data.find((d) => d.key_as_string === key)?.doc_count ?? 0;
      return { key, doc_count };
    });
  });
</script>

<div class="h-6 w-full">
  <BarChart
    data={chart}
    x="key"
    y="doc_count"
    axis={false}
    grid={false}
    bandPadding={0.1}
    props={{
      bars: {
        class: "fill-blue-500",
        radius: 1,
        strokeWidth: 0,
      },
      highlight: {
        area: {
          class: "fill-zinc-200/50 rounded",
        },
      },
    }}
  >
    <svelte:fragment slot="tooltip" let:x let:y>
      <Tooltip.Root
        let:data
        class="rounded border border-zinc-300 bg-white shadow"
      >
        <Tooltip.Header class="border-zinc-300">
          {x(data)}
        </Tooltip.Header>
        <Tooltip.List>
          <Tooltip.Item label="Aantal" value={formatNumber(y(data))} />
        </Tooltip.List>
      </Tooltip.Root>
    </svelte:fragment>
  </BarChart>
</div>
