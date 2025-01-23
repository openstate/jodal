<script lang="ts">
  import { enhance } from "$app/forms";
  import { page } from "$app/stores";

  const id = $derived($page.url.searchParams.get("id"));

  let { form } = $props();
</script>

<form method="POST" use:enhance class="space-y-4">
  <h1 class="text-lg font-medium">Wachtwoord veranderen</h1>

  {#if form?.message || !id}
    <div
      class="rounded border border-red-900/20 bg-red-100 px-4 py-3 text-red-950"
    >
      {#if !id}
        <p>Je kan niet je wachtwoord veranderen zonder geldige code.</p>
      {:else}
        <p>{form?.message}</p>
      {/if}
    </div>
  {/if}

  <input type="hidden" name="changePasswordId" value={id} />
  <input
    type="password"
    name="password"
    placeholder="Nieuw wachtwoord"
    class="w-full rounded border border-stone-300 px-4 py-3 focus:border-stone-400 focus:outline-0"
  />
  <input
    type="password"
    name="password_repeat"
    placeholder="Herhaal nieuw wachtwoord"
    class="w-full rounded border border-stone-300 px-4 py-3 focus:border-stone-400 focus:outline-0"
  />

  <div class="flex justify-end">
    <button
      class="pt-1.75 cursor-pointer rounded-lg bg-black px-4 pb-2 font-bold text-white"
    >
      Verander wachtwoord
    </button>
  </div>
</form>
