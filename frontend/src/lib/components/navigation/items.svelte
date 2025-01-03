<script lang="ts">
  import Search from "@tabler/icons-svelte/icons/search";
  import Home_2 from "@tabler/icons-svelte/icons/home-2";
  import Planet from "@tabler/icons-svelte/icons/planet";
  import MessageCircle from "@tabler/icons-svelte/icons/message-circle";
  import ExternalLink from "@tabler/icons-svelte/icons/external-link";
  import Bookmarks from "@tabler/icons-svelte/icons/bookmarks";
  import { page } from "$app/state";

  type Props = { onclick?: () => void; maxFeeds?: number };
  let { onclick, maxFeeds = 5 }: Props = $props();
</script>

<a
  href="/zoeken"
  class="mx-2 my-2 flex cursor-pointer gap-2.5 rounded-lg border-2 border-stone-200 bg-white px-3 py-2 text-stone-700 transition-colors hover:border-stone-300"
  {onclick}
>
  <Search class="w-4.5" />
  Zoeken
</a>
<a
  class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
  href="/app"
  {onclick}
>
  <Home_2 class="w-5 text-stone-800" />
  Home
</a>
<a
  class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
  href="/app"
  {onclick}
>
  <Planet class="w-5 text-stone-800" />
  Ontdekken
</a>
<a
  class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
  href="/feeds"
  {onclick}
>
  <Bookmarks class="w-5 text-stone-800" />
  Feeds
</a>
<div
  class="my-1 ml-6 border-l-2 border-l-stone-200 pl-2 font-sans text-stone-700"
>
  {#each page.data.feeds?.slice(0, maxFeeds) ?? [] as feed}
    <a
      class="mx-2 block rounded px-3 py-1 text-sm capitalize transition-colors hover:bg-stone-50"
      href="/feeds/{feed.public_id}"
      {onclick}
    >
      {feed.name}
    </a>
  {/each}
  {#if page.data.feeds && page.data.feeds.length > maxFeeds}
    <a
      class="mx-2 block rounded px-3 py-1 text-sm font-medium transition-colors hover:bg-stone-50"
      href="/feeds"
      {onclick}
    >
      Alle {page.data.feeds.length} feeds...
    </a>
  {/if}
</div>
<a
  class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
  href="//chat.bron.live"
  target="_blank"
  {onclick}
>
  <MessageCircle class="w-5 text-stone-800" />
  Chat
  <ExternalLink class="ml-auto w-4 text-stone-500" />
</a>
