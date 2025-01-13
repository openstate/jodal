<script lang="ts">
  import { afterNavigate } from "$app/navigation";
  import SideBar from "$lib/components/navigation/side-bar.svelte";
  import TopBar from "$lib/components/navigation/top-bar.svelte";

  let { children } = $props();

  // Override default scroll restoration, because SvelteKit by default only
  // fixes scroll for `window`, but `article#scroll` is our scroll container.
  afterNavigate(() => {
    document.getElementById("scroll")!.scrollTo(0, 0);
  });
</script>

<svelte:head>
  <title>Bron</title>
  <meta property="og:title" content="Bron" />
</svelte:head>

<main class="grid h-dvh">
  <TopBar />
  <SideBar />
  <article id="scroll" class="overflow-y-scroll px-4 py-8">
    <div class="lg:max-w-300 lg:mx-auto">
      {@render children?.()}
    </div>
  </article>
</main>

<style>
  main {
    @media (width < 64rem) {
      grid-template-rows: 4rem 1fr;
    }

    @media (width >= 64rem) {
      grid-template-columns: 18rem 1fr;
    }
  }
</style>
