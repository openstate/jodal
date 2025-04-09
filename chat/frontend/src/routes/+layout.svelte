<script>
  import "../app.css";
  import Header from '$lib/components/Header.svelte';

  // Remove the conditional header rendering
</script>

<Header />

<main>
  <slot />
</main>

<style>
  main {
    min-height: 100vh;
  }
</style>