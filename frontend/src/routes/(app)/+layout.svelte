<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg";
  import Logout from "@tabler/icons-svelte/icons/logout";

  import { enhance } from "$app/forms";

  import Search from "@tabler/icons-svelte/icons/search";
  import Home_2 from "@tabler/icons-svelte/icons/home-2";
  import Planet from "@tabler/icons-svelte/icons/planet";
  import MessageCircle from "@tabler/icons-svelte/icons/message-circle";
  import ExternalLink from "@tabler/icons-svelte/icons/external-link";
  import LayersSubtract from "@tabler/icons-svelte/icons/layers-subtract";

  let { data, children } = $props();
</script>

<svelte:head>
  <title>Bron</title>
  <meta property="og:title" content="Bron" />
</svelte:head>

<main class="grid h-screen grid-cols-[16rem_1fr]">
  <nav class="flex h-full flex-col border-r-2 border-stone-200 bg-white p-4">
    <div class="grow font-display">
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
        class="flex items-center gap-2.5 rounded px-4 py-2 transition-colors hover:bg-stone-100"
        href="/"
      >
        <Home_2 class="w-5 text-stone-800" />
        Home
      </a>
      <a
        class="flex items-center gap-2.5 rounded px-4 py-2 transition-colors hover:bg-stone-100"
        href="/"
      >
        <Planet class="w-5 text-stone-800" />
        Ontdekken
      </a>
      <a
        class="flex items-center gap-2.5 rounded px-4 py-2 transition-colors hover:bg-stone-100"
        href="/feeds"
      >
        <LayersSubtract class="w-5 text-stone-800" />
        Feeds
      </a>
      <div class="my-1 font-sans ml-6 border-l-2 border-l-stone-200 pl-2 text-stone-700">
        {#each data.feeds ?? [] as feed}
          <a
            class="block rounded px-3 py-1 text-sm capitalize transition-colors hover:bg-stone-50"
            href="/feeds/{feed.public_id}"
          >
            {feed.name}
          </a>
        {/each}
      </div>
      <a
        class="flex items-center gap-2.5 rounded px-4 py-2 transition-colors hover:bg-stone-100"
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
          <p class="grow truncate px-4 font-semibold">
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
  <article class="overflow-y-scroll p-8">
    <div class="max-w-300 mx-auto">
      {@render children?.()}
    </div>
  </article>
</main>
