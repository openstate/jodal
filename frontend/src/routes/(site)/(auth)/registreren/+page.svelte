<script lang="ts">
  import { enhance } from "$app/forms";

  let { form } = $props();
</script>

<form method="POST" use:enhance class="space-y-4">
  <h1 class="font-display text-lg font-medium">Registreren</h1>

  {#if form?.message}
    <div
      class="rounded border px-4 py-3 {form.success === false
        ? 'border-red-900/20 bg-red-100 text-red-950'
        : 'border-stone-200 bg-stone-100 text-stone-900'}"
    >
      <p>{form.message}</p>
    </div>
  {/if}

  <input
    type="email"
    name="email"
    placeholder="E-mailadres"
    class="w-full rounded border border-stone-200 px-4 py-3 focus:border-stone-400 focus:outline-0"
  />
  <input
    type="password"
    name="password"
    placeholder="Wachtwoord"
    class="w-full rounded border border-stone-200 px-4 py-3 focus:border-stone-400 focus:outline-0"
  />
  <div class="flex justify-end">
    <button
      class="pt-1.75 cursor-pointer rounded-lg bg-purple-700 px-4 pb-2 font-bold text-white"
    >
      Registreer
    </button>
  </div>
</form>
