<script>
 import { slide } from "svelte/transition";
 //import { openAccordian } from "./AccordionStore.js";
 import { createEventDispatcher } from "svelte";
 const dispatch = createEventDispatcher();

 export let id = 0;
 export let openedAccordion = 0;
 // function setOpenAccordian(value) {
 //   openAccordian.update(n => (n == value ? 0 : value));
 // }
</script>

<style>
  .collapsible-body {
    display: block;
  }
</style>
<!-- on:click={()=>setOpenAccordian(id)} -->
<div class="collapsible-header" on:click={() => dispatch('accordionSelected', id)} >
  <slot name="title"  />
</div>

{#if id == openedAccordion }
  <div class="collapsible-body" transition:slide|local>
      <slot />
  </div>
{/if}

        