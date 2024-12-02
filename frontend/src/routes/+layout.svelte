<script lang="ts">
  import "../app.css";

  import BronLogo from "$lib/assets/bron-logo.svg";
  import Logout from "@tabler/icons-svelte/icons/logout";

  import { identity } from "$lib/stores";
  import { enhance } from "$app/forms";

  let { children } = $props();
</script>

<svelte:head>
  <title>Bron</title>
  <meta property="og:title" content="Bron" />
</svelte:head>

{#snippet link(href: string, name: string)}
  <a class="block rounded px-4 py-2 transition-colors hover:bg-gray-100" {href}>
    {name}
  </a>
{/snippet}

<main class="grid h-screen grid-cols-[16rem_1fr]">
  <nav class="flex h-full flex-col border-r-2 border-gray-200 p-4">
    <div class="grow">
      <a class="inline-block p-4" href="/">
        <img src={BronLogo} class="w-32" alt="Bron Logo" />
      </a>
      {@render link("/", "Home")}
      {@render link("/zoeken", "Zoeken")}
      {@render link("/feeds", "Feeds")}
    </div>
    <div>
      {#if $identity}
        <div class="flex rounded border-2 border-gray-200 py-2">
          <p class="grow truncate px-4 font-semibold">
            {$identity.email}
          </p>
          <form method="POST" action="/logout" use:enhance class="contents">
            <button class="shrink-0 cursor-pointer">
              <Logout class="mx-2 w-5" />
            </button>
          </form>
        </div>
      {:else}
        <div class="space-y-2">
          <a
            href="/login"
            class="flex cursor-pointer items-center justify-center rounded bg-gray-200 py-2 font-semibold"
          >
            Inloggen
          </a>
          <a
            href="/register"
            class="flex cursor-pointer items-center justify-center rounded border-2 border-gray-200 py-2"
          >
            Registreren
          </a>
        </div>
      {/if}
    </div>
  </nav>
  <article class="overflow-y-scroll p-8">
    {@render children?.()}
  </article>
</main>
