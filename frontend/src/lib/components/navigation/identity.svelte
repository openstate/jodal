<script lang="ts">
  import { enhance } from "$app/forms";
  import { page } from "$app/state";
  import { IconLogout } from "@tabler/icons-svelte";
</script>

{#if page.data.identity}
  <div
    class="flex items-center justify-between overflow-hidden rounded-lg border border-stone-300 text-center text-stone-800"
  >
    <span class="grow truncate py-3 pl-4">{page.data.identity.email}</span>
    <form method="POST" action="/uitloggen" use:enhance class="contents">
      <button
        class="shrink-0 cursor-pointer px-4 opacity-80 transition-opacity hover:opacity-100"
        title="Uitloggen"
      >
        <IconLogout class="size-5" />
      </button>
    </form>
  </div>
{:else}
  <div class="grid gap-3 max-lg:grid-cols-2">
    <a
      href="/inloggen"
      class="cursor-pointer rounded-lg border border-stone-300 px-4 py-3 text-center text-stone-800 transition hover:bg-stone-50 disabled:opacity-50"
    >
      Inloggen
    </a>
    <a
      href="/registreren"
      class="cursor-pointer rounded-lg bg-black px-4 py-3 text-center font-semibold text-white transition hover:bg-stone-800 disabled:opacity-50"
    >
      Registreren
    </a>
  </div>
{/if}
