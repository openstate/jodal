<script lang="ts">
  import { enhance } from "$app/forms";
  import { page } from "$app/stores";

  const id = $derived($page.url.searchParams.get("id"));

  let { form } = $props();
</script>

<svelte:head>
  <title>Wachtwoord veranderen &ndash; Bron</title>
</svelte:head>

<form
  method="POST"
  use:enhance
  class="max-w-120 m-2 mx-auto mt-20 w-full space-y-4 rounded-lg border border-stone-300 bg-white p-8"
>
  {#if !form?.success}
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
        class="pt-1.75 cursor-pointer rounded-lg bg-stone-900 px-4 pb-2 font-bold text-white transition hover:bg-stone-800"
      >
        Verander wachtwoord
      </button>
    </div>
  {:else}
    <h1 class="text-lg font-medium">Wachtwoord veranderd</h1>

    <p class="text-stone-700">
      Jouw wachtwoord is veranderd! Dat betekent dat je nu kunt inloggen op
      Bron.
    </p>

    <a
      href="/inloggen"
      class="block w-fit cursor-pointer rounded-lg bg-stone-900 px-4 pb-2 pt-2 font-bold text-white transition hover:bg-stone-800"
    >
      Inloggen
    </a>
  {/if}
</form>
