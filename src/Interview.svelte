<script>
import { onMount, onDestroy } from 'svelte';
import { fade, slide } from 'svelte/transition';
</script>
<section class="column-section" out:fade>
<div id="column-interview" class="column">
  <div id="column-contents-interview" class="column-contents">
    <div id="wufoo-form-loading" class="loading"></div>
    <iframe height="799" onload="document.getElementById('wufoo-form-loading').style.display='none';" title="Embedded Wufoo Form" allowtransparency="true" frameborder="0" scrolling="no" style="width:100%;border:none" sandbox="allow-top-navigation allow-scripts allow-popups allow-forms allow-same-origin" src="https://jodal.wufoo.com/embed/zekl9wu16ytpmk/"> <a href="https://jodal.wufoo.com/forms/zekl9wu16ytpmk/">Fill out my Wufoo form!</a> </iframe>
  </div>
</div>
</section>
