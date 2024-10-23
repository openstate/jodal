<script>
  import { onMount } from 'svelte';
  import '../scss/variables.scss';
  //import "../scss/bootstrap.scss";
  import '../scss/tabler.scss';
  import '../scss/app.scss';
  import { browser } from '$app/environment';
  import NavBar from '$lib/NavBar.svelte';

  onMount(async () => {
    if (!browser) return;
    //await import("bootstrap");
    await import('@tabler/core');
  });
</script>

<svelte:head>
  <title>Bron</title>
  <meta property="og:title" content="Bron" />
</svelte:head>

<NavBar />
<main class="mt-3 mb-5">
  <div class="container">
    <slot />
  </div>
</main>
