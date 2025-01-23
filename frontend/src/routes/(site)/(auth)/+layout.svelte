<script lang="ts">
  let { children } = $props();
</script>

<div class="py-36 md:py-48 px-6">
  <div
    class="max-w-120 m-2 mx-auto mt-20 w-full rounded-lg border border-stone-300 bg-white p-8"
  >
    {@render children?.()}
  </div>
</div>
