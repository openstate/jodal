<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg";
  import Logout from "@tabler/icons-svelte/icons/logout";

  import { enhance } from "$app/forms";

  import Items from "./items.svelte";
    import { page } from "$app/state";
</script>

<nav
  class="flex h-full flex-col border-r-2 border-stone-200 bg-white p-4 max-sm:hidden"
>
  <div class="font-display grow">
    <a class="inline-block p-4" href="/">
      <img src={BronLogo} class="w-36" alt="Bron Logo" />
    </a>
    <Items />
  </div>
  <div>
    {#if page.data.identity}
      <div class="flex rounded border-2 border-stone-200 py-2">
        <p class="mx-2 grow truncate px-2 font-semibold">
          {page.data.identity.email}
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
