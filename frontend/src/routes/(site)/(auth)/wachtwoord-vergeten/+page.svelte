<script lang="ts">
  import { enhance } from "$app/forms";

  let { form } = $props();
</script>

<form method="POST" use:enhance class="max-w-120 m-2 mx-auto mt-20 w-full rounded-lg border border-stone-300 bg-white p-8 space-y-4">
  <h1 class="text-lg font-medium">Wachtwoord vergeten</h1>

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
  <div class="flex justify-end">
    <button
      class="pt-1.75 cursor-pointer rounded-lg bg-black px-4 pb-2 font-bold text-white"
    >
      Stuur bevestiging
    </button>
  </div>
</form>
