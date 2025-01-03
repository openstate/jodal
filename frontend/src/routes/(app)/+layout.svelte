<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg";
  import LayersSubtract from "@tabler/icons-svelte/icons/layers-subtract";
  import Sidebar from "./sidebar.svelte";
  import Planet from "@tabler/icons-svelte/icons/planet";
  import Home_2 from "@tabler/icons-svelte/icons/home-2";
  import Search from "@tabler/icons-svelte/icons/search";
  import MessageCircle from "@tabler/icons-svelte/icons/message-circle";
  import { page } from "$app/state";
  import Bookmarks from "@tabler/icons-svelte/icons/bookmarks";

  let { data, children } = $props();
</script>

<svelte:head>
  <title>Bron</title>
  <meta property="og:title" content="Bron" />
</svelte:head>

<main class="grid h-screen">
  <nav
    class="flex items-center border-b-2 border-stone-200 bg-white px-2 [grid-area:topbar] sm:hidden"
  >
    <a class="inline-block p-4" href="/">
      <img src={BronLogo} class="w-28" alt="Bron Logo" />
    </a>
  </nav>
  <Sidebar {data} />
  <article class="overflow-y-scroll p-4 [grid-area:content]">
    <div class="sm:max-w-300 sm:mx-auto">
      {@render children?.()}
    </div>
  </article>
  <nav
    class="grid grid-flow-col items-center justify-around border-t-2 border-stone-200 bg-white px-4 [grid-area:bottombar] sm:hidden"
  >
    <a class="flex items-center gap-2" href="/">
      <Home_2 class="w-6 text-stone-800" />
    </a>

    <a class="flex items-center gap-2" href="/zoeken">
      <Search class="w-6 text-stone-800" />
    </a>
    <a class="flex items-center gap-2" href="/feeds">
      <Bookmarks class="w-6 text-stone-800" />
    </a>
    <a class="flex items-center gap-2" href="/">
      <Planet class="w-6 text-stone-800" />
    </a>
  </nav>
</main>

<style>
  @media (width < 40rem) {
    main {
      grid-template-areas: "topbar" "content" "bottombar";
      grid-template-rows: 4rem 1fr 4rem;
    }
  }

  @media (width >= 40rem) {
    main {
      grid-template-areas: "sidebar content";
      grid-template-columns: 18rem 1fr;
    }
  }
</style>
