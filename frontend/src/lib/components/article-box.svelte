<script lang="ts">
  import ArrowRight from "@tabler/icons-svelte/icons/arrow-right";

  type Props = {
    image: string;
    slug: string;
    title: string;
    description: string;
    tag?: string;
    highlight: string;
  };

  let { image, slug, title, highlight, tag }: Props = $props();
</script>

<a
  href="/gids/{slug}"
  class="group flex flex-col rounded-2xl border border-stone-300 transition hover:bg-stone-100"
>
  <div class=" rounded-t-2xl bg-blue-600">
    <img
      src={image}
      alt={title}
      class="h-32 w-full rounded-t-2xl object-cover opacity-75 transition group-hover:opacity-90"
      loading="lazy"
    />
  </div>
  <div class="p-8 pb-0">
    <h4 class="font-display mb-2 text-xl font-medium">{title}</h4>
    <p class="mb-4 text-stone-700">
      {highlight}
    </p>
  </div>
  <div class="mx-8 mb-8 flex grow items-end">
    <div
      class="flex ml-au w-fit items-center gap-2 rounded-full bg-blue-100 px-3 py-0.5 text-blue-900"
    >
      <ArrowRight class="size-4" /> Lees meer
    </div>
  </div>
</a>
