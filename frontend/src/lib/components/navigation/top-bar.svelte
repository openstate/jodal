<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg";
  import Logout from "@tabler/icons-svelte/icons/logout";

  import { enhance } from "$app/forms";

  import Menu_2 from "@tabler/icons-svelte/icons/menu-2";
  import Close from "@tabler/icons-svelte/icons/x";
  import Items from "./items.svelte";

  let menuOpen = $state(false);

  let menuClass = $derived(menuOpen ? "opacity-0 rotate-90" : "");
  let closeClass = $derived(menuOpen ? "" : "opacity-0 -rotate-90");
</script>

<nav
  class={[
    "z-50 flex items-center justify-between border-b bg-white px-6 transition lg:hidden",
    menuOpen ? "border-white" : "border-stone-300",
  ]}
>
  <a class="inline-block" href="/" onclick={() => (menuOpen = false)}>
    <img src={BronLogo} class="w-30" alt="Bron Logo" />
  </a>
  <button
    class="relative flex h-7 w-7 items-center justify-center"
    onclick={() => (menuOpen = !menuOpen)}
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
    "fixed left-0 top-16 z-40 w-full border-b border-stone-300 bg-white p-4 pt-0 transition duration-300 lg:hidden",
    !menuOpen && "-translate-y-full",
  ]}
>
  <Items onclick={() => (menuOpen = false)} maxFeeds={3} maxArticles={3} />
</div>

<div
  onclick={() => (menuOpen = false)}
  class={[
    "fixed z-30 h-dvh w-dvw bg-black/50 transition duration-300 lg:hidden",
    menuOpen ? "" : "pointer-events-none opacity-0",
  ]}
></div>
