<script lang="ts">
  import { enhance } from "$app/forms";
  import { page } from "$app/state";
  import Logout from "@tabler/icons-svelte/icons/logout";
</script>

{#if page.data.identity}
  <div class="flex rounded border border-stone-300 py-2">
    <p class="mx-2 grow truncate px-2 font-medium">
      {page.data.identity.email}
    </p>
    <form method="POST" action="/uitloggen" use:enhance class="contents">
      <button class="shrink-0 cursor-pointer" title="Uitloggen">
        <Logout class="mx-2 w-5" />
      </button>
    </form>
  </div>
{/if}
