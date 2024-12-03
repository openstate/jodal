<script lang="ts">
  let { children } = $props();
</script>

<div
  class="max-w-120 m-2 mx-auto w-full rounded-lg border border-stone-200 bg-white p-8"
>
  {@render children?.()}
</div>
