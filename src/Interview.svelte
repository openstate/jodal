<script>
import { onMount, onDestroy } from 'svelte';
import { fade, slide } from 'svelte/transition';
</script>
<section class="column-section" out:fade>
<div id="column-interview" class="column">
  <div class="column-title">
    <h2>Enquete</h2>
  </div>
  <div id="column-contents-interview" class="column-contents">
  Hier willen we interview vragen.
  </div>
</div>
</section>
