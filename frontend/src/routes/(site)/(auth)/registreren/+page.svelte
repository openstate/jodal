<script lang="ts">
  import { enhance } from "$app/forms";
  import { createFormState } from "$lib/utils.svelte";

  let { form } = $props();

  let state = createFormState();
</script>

<svelte:head>
  <title>Registreren &ndash; Bron</title>
</svelte:head>

<form
  method="POST"
  use:enhance={state.submit}
  class="max-w-120 m-2 mx-auto mt-20 grid w-full gap-y-4 rounded-lg border border-stone-300 bg-white p-8"
>
  <div class="mb-2">
    <h1 class="mb-2 text-lg font-medium">Registreren</h1>

    <p class="text-stone-700">
      Met een gratis Bron-account kun je oneindig vaak documenten uit alle
      bestuurslagen doorzoeken en blijf je via feeds altijd op de hoogte van
      nieuwe documenten.
    </p>
  </div>

  {#if form?.message}
    <div
      class="rounded border px-4 py-3 {form.success === false
        ? 'border-red-900/20 bg-red-100 text-red-950'
        : 'border-stone-300 bg-stone-100 text-stone-900'}"
    >
      <p>{form.message}</p>
    </div>
  {/if}

  <input
    type="email"
    name="email"
    placeholder="E-mailadres"
    class="w-full rounded border border-stone-300 px-4 py-3 focus:border-stone-400 focus:outline-0"
  />
  <input
    type="password"
    name="password"
    placeholder="Nieuw wachtwoord"
    class="w-full rounded border border-stone-300 px-4 py-3 focus:border-stone-400 focus:outline-0"
  />
  <div class="flex justify-end">
    <button
      class="pt-1.75 not-disabled:cursor-pointer not-disabled:hover:bg-stone-800 rounded-lg bg-stone-900 px-4 pb-2 font-bold text-white"
      class:animate-pulse={state.loading}
      disabled={state.loading}
    >
      Log in
    </button>
  </div>
</form>

<p class="mt-8 text-center font-[350] text-stone-600">
  Al een account? <a href="/inloggen" class="underline">Log in</a>.
</p>
