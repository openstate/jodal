<script lang="ts">
  import type { Snippet } from "svelte";

  type Props = { open: boolean; children: Snippet };
  let { open = $bindable(), children }: Props = $props();

  let dialog: HTMLDialogElement;

  $effect(() => {
    if (open) dialog.showModal();
    else dialog.close();
  });
</script>

<dialog
  class="[:modal]:max-w-screen [:modal]:max-h-screen [:modal]:size-full [:modal]:overflow-hidden relative bg-transparent backdrop:bg-black/50"
  bind:this={dialog}
  onclose={() => (open = false)}
  oncancel={() => (open = false)}
>
  {@render children()}
</dialog>
