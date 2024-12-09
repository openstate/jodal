<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg";
  import Logout from "@tabler/icons-svelte/icons/logout";

  import { enhance } from "$app/forms";

  let { data, children } = $props();
</script>

<svelte:head>
  <title>Bron</title>
  <meta property="og:title" content="Bron" />
</svelte:head>

{#snippet link(href: string, name: string)}
  <a
    class="block rounded px-4 py-2 transition-colors hover:bg-stone-100"
    {href}
  >
    {name}
  </a>
{/snippet}

<main class="grid h-screen grid-cols-[16rem_1fr]">
  <nav class="flex h-full flex-col border-r-2 border-stone-200 bg-white p-4">
    <div class="grow">
      <a class="inline-block p-4" href="/">
        <img src={BronLogo} class="w-42" alt="Bron Logo" />
      </a>
      {@render link("/", "Home")}
      {@render link("/zoeken", "Zoeken")}
      {@render link("/feeds", "Feeds")}
      {#each data.feeds ?? [] as feed}
        {@render link(
          `/feeds/${feed.public_id}`,
          `Feed '${feed.name}'`,
        )}
      {/each}
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
