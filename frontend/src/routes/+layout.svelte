<script lang="ts">
  import "../app.css";
  import Matomo from "./matomo.svelte";

  let { children } = $props();
</script>

<svelte:head>
  <title>Bron &ndash; Superkrachten voor journalisten</title>
</svelte:head>

<Matomo />

{@render children?.()}
