<script lang="ts">
  import SideBar from "$lib/components/navigation/side-bar.svelte";
  import TopBar from "$lib/components/navigation/top-bar.svelte";

  let { children } = $props();
</script>

<svelte:head>
  <title>Bron</title>
  <meta property="og:title" content="Bron" />
</svelte:head>

<main class="grid h-dvh">
  <TopBar />
  <SideBar />
  <article class="overflow-y-scroll p-4">
    <div class="sm:max-w-300 sm:mx-auto">
      {@render children?.()}
    </div>
  </article>
</main>

<style>
  main {
    @media (width < 40rem) {
      grid-template-rows: 4rem 1fr;
    }

    @media (width >= 40rem) {
      grid-template-columns: 18rem 1fr;
    }
  }
</style>
