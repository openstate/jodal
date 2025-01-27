<script lang="ts">
  import "../app.css";
  import Matomo from "./matomo.svelte";

  let { children } = $props();
</script>

<Matomo />

{@render children?.()}
