<div class="block rounded-lg border border-stone-300 bg-white p-4">
  <div class="mb-3 mt-1 h-4 w-80 animate-pulse rounded bg-stone-300"></div>
  <div class="mb-2 h-4 animate-pulse rounded bg-stone-200"></div>
  <div class="mb-2 h-4 animate-pulse rounded bg-stone-200"></div>
  <div class="w-1/2 h-4 animate-pulse rounded bg-stone-200"></div>
  <div class="mt-3 flex gap-2">
    {#each { length: 3 } as _}
      <div class="w-32 max-w-full h-7 animate-pulse rounded bg-stone-200/75"></div>
    {/each}
  </div>
</div>
