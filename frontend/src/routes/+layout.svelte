<script lang="ts">
  import { onMount, type Snippet } from 'svelte';
  import '../scss/variables.scss';
  //import "../scss/bootstrap.scss";
  import '../scss/tabler.scss';
  import '../scss/app.scss';
  import { browser } from '$app/environment';
  import NavBar from '$lib/NavBar.svelte';
  import { QueryClientProvider, QueryClient } from '@tanstack/svelte-query';

  const queryClient = new QueryClient({})

  let { children }: { children: Snippet }= $props();

  onMount(async () => {
    if (!browser) return;
    //await import("bootstrap");
    // @ts-expect-error
    await import('@tabler/core');
  });
</script>

<svelte:head>
  <title>Bron</title>
  <meta property="og:title" content="Bron" />
</svelte:head>

<QueryClientProvider client={queryClient}>
  <NavBar />
  <main class="mt-3 mb-5">
    <div class="container">
      {@render children?.()}
    </div>
  </main>
</QueryClientProvider>
