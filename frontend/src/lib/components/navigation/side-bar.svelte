<script lang="ts">
  import BronLogo from "$lib/assets/bron-logo.svg";
  import Items from "./items.svelte";
  import { IconX } from "@tabler/icons-svelte";
  import { onMount } from "svelte";
  import Identity from "./identity.svelte";

  let messageDismissed = $state(true);

  onMount(() => {
    if (!localStorage.getItem("bron-welcome-message-dismissed")) {
      messageDismissed = false;
    }
  });

  let dismissMessage = () => {
    localStorage.setItem("bron-welcome-message-dismissed", "true");
    messageDismissed = true;
  };

  $inspect(messageDismissed);
</script>

<nav
  class="flex h-full flex-col border-r border-stone-300 bg-white p-4 max-lg:hidden"
>
  <div class=" grow">
    <a class="inline-block p-4" href="/">
      <img src={BronLogo} class="w-36" alt="Bron Logo" />
    </a>
    <Items />
  </div>
  <div class="grid gap-3">
    {#if !messageDismissed}
      <div
        class="fade-in rounded border border-stone-300 px-4 py-2 text-stone-800"
      >
        <div class="flex items-center justify-between">
          <p class="my-1 font-medium">Welkom bij Bron!</p>
          <button
            onclick={dismissMessage}
            class="cursor-pointer opacity-80 transition-opacity hover:opacity-100"
            title="Sluiten"
          >
            <IconX class="size-4" />
          </button>
        </div>
        <p>
          Bron is altijd in beweging. Kom je ergens niet uit, of heb je
          suggesties? Stuur een mailtje naar
          <a href="mailto:jan@openstate.eu" target="_blank" class="underline">
            jan@openstate.eu
          </a>.
        </p>
      </div>
    {/if}
    <Identity />
  </div>
</nav>

<style>
  .fade-in {
    animation: fadeIn 100ms ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
</style>
