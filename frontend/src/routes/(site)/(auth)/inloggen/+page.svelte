<script lang="ts">
  import { enhance } from "$app/forms";
  import { navigating } from "$app/state";
  import { createFormState } from "$lib/utils.svelte";

  let { form } = $props();

  let state = createFormState();

  // true if either the form is submitting or the search page is loading
  let loading = $derived(
    state.loading || navigating.to?.url.pathname == "/zoeken",
  );
</script>

<svelte:head>
  <title>Inloggen &ndash; Bron</title>
</svelte:head>

<form
  method="POST"
  use:enhance={state.submit}
  class="max-w-120 m-2 mx-auto mt-20 w-full space-y-4 rounded-lg border border-stone-300 bg-white p-8"
>
  <h1 class="text-lg font-medium">Inloggen</h1>

  {#if form?.success === false}
    <div
      class="rounded border border-red-900/20 bg-red-100 px-4 py-3 text-red-950"
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
    placeholder="Wachtwoord"
    class="w-full rounded border border-stone-300 px-4 py-3 focus:border-stone-400 focus:outline-0"
  />
  <div class="flex items-center justify-between">
    <a
      href="/wachtwoord-vergeten"
      class="font-[350] text-stone-600 hover:underline"
    >
      Wachtwoord vergeten?
    </a>
    <button
      class="pt-1.75 not-disabled:cursor-pointer not-disabled:hover:bg-stone-800 rounded-lg bg-stone-900 px-4 pb-2 font-bold text-white"
      class:animate-pulse={loading}
      disabled={loading}
    >
      Log in
    </button>
  </div>
</form>

<p class="mt-8 text-center font-[350] text-stone-600">
  Nog geen account? <a href="/registreren" class="underline">Registreer</a>.
</p>
