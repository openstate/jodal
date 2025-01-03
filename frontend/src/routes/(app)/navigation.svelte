<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg";
  import Logout from "@tabler/icons-svelte/icons/logout";

  import { enhance } from "$app/forms";

  import Search from "@tabler/icons-svelte/icons/search";
  import Home_2 from "@tabler/icons-svelte/icons/home-2";
  import Planet from "@tabler/icons-svelte/icons/planet";
  import MessageCircle from "@tabler/icons-svelte/icons/message-circle";
  import ExternalLink from "@tabler/icons-svelte/icons/external-link";
  import Bookmarks from "@tabler/icons-svelte/icons/bookmarks";
  import Menu_2 from "@tabler/icons-svelte/icons/menu-2";
  import Close from "@tabler/icons-svelte/icons/x";

  let { data } = $props();

  const MAX_SIDEBAR_FEEDS = 5;

  let sidebarOpen = $state(false);

  let menuClass = $derived(sidebarOpen ? "opacity-0 rotate-90" : "");
  let closeClass = $derived(sidebarOpen ? "" : "opacity-0 -rotate-90");
</script>

<!-- Mobile -->
<nav
  class="z-50 flex items-center justify-between border-b-2 border-stone-200 bg-white px-4 sm:hidden"
>
  <a class="inline-block" href="/">
    <img src={BronLogo} class="w-30" alt="Bron Logo" />
  </a>
  <button
    class="relative flex h-10 w-10 items-center justify-center"
    onclick={() => (sidebarOpen = !sidebarOpen)}
  >
    <div class="absolute transition {menuClass}">
      <Menu_2 class="size-7 text-stone-700" />
    </div>
    <div class="absolute transition {closeClass}">
      <Close class="size-7 text-stone-700" />
    </div>
  </button>
</nav>

<div
  class={[
    "fixed left-0 top-16 z-40 w-full border-b-2 border-stone-200 bg-white p-4 transition sm:hidden",
    !sidebarOpen && "-translate-y-full",
  ]}
>
  <a
    href="/zoeken"
    class="mx-2 my-2 flex cursor-pointer gap-2.5 rounded-lg border-2 border-stone-200 bg-white px-3 py-2 text-stone-700 transition-colors hover:border-stone-300"
    onclick={() => (sidebarOpen = false)}
  >
    <Search class="w-4.5" />
    Zoeken
  </a>
  <a
    class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
    href="/"
    onclick={() => (sidebarOpen = false)}
  >
    <Home_2 class="w-5 text-stone-800" />
    Home
  </a>
  <a
    class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
    href="/"
    onclick={() => (sidebarOpen = false)}
  >
    <Planet class="w-5 text-stone-800" />
    Ontdekken
  </a>
  <a
    class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
    href="/feeds"
    onclick={() => (sidebarOpen = false)}
  >
    <Bookmarks class="w-5 text-stone-800" />
    Feeds
  </a>

  <a
    class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
    href="//chat.bron.live"
    target="_blank"
    onclick={() => (sidebarOpen = false)}
  >
    <MessageCircle class="w-5 text-stone-800" />
    Chat
    <ExternalLink class="ml-auto w-4 text-stone-500" />
  </a>
</div>

<div
  class={[
    "fixed z-30 h-dvh w-dvw bg-black/50 transition",
    sidebarOpen ? "" : "pointer-events-none opacity-0",
  ]}
></div>

<!-- Desktop -->
<nav
  class="flex h-full flex-col border-r-2 border-stone-200 bg-white p-4 max-sm:hidden"
>
  <div class="font-display grow">
    <a class="inline-block p-4" href="/">
      <img src={BronLogo} class="w-36" alt="Bron Logo" />
    </a>
    <a
      href="/zoeken"
      class="mx-2 my-2 flex cursor-pointer gap-2.5 rounded-lg border-2 border-stone-200 bg-white px-3 py-2 text-stone-700 transition-colors hover:border-stone-300"
    >
      <Search class="w-4.5" />
      Zoeken
    </a>
    <a
      class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
      href="/"
    >
      <Home_2 class="w-5 text-stone-800" />
      Home
    </a>
    <a
      class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
      href="/"
    >
      <Planet class="w-5 text-stone-800" />
      Ontdekken
    </a>
    <a
      class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
      href="/feeds"
    >
      <Bookmarks class="w-5 text-stone-800" />
      Feeds
    </a>
    <div
      class="my-1 ml-6 border-l-2 border-l-stone-200 pl-2 font-sans text-stone-700"
    >
      {#each data.feeds?.slice(0, MAX_SIDEBAR_FEEDS) ?? [] as feed}
        <a
          class="mx-2 block rounded px-3 py-1 text-sm capitalize transition-colors hover:bg-stone-50"
          href="/feeds/{feed.public_id}"
        >
          {feed.name}
        </a>
      {/each}
      {#if data.feeds && data.feeds.length > MAX_SIDEBAR_FEEDS}
        <a
          class="mx-2 block rounded px-3 py-1 text-sm font-medium transition-colors hover:bg-stone-50"
          href="/feeds"
        >
          Alle {data.feeds.length} feeds...
        </a>
      {/if}
    </div>
    <a
      class="mx-2 flex items-center gap-2.5 rounded px-2 py-2 transition-colors hover:bg-stone-100"
      href="//chat.bron.live"
      target="_blank"
    >
      <MessageCircle class="w-5 text-stone-800" />
      Chat
      <ExternalLink class="ml-auto w-4 text-stone-500" />
    </a>
  </div>
  <div>
    {#if data.identity}
      <div class="flex rounded border-2 border-stone-200 py-2">
        <p class="mx-2 grow truncate px-2 font-semibold">
          {data.identity.email}
        </p>
        <form method="POST" action="/uitloggen" use:enhance class="contents">
          <button class="shrink-0 cursor-pointer">
            <Logout class="mx-2 w-5" />
          </button>
        </form>
      </div>
    {/if}
  </div>
</nav>
