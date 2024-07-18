<script>
  import { identity, apiDomainName } from '$lib/stores';
  import { Mastodon, TwitterX, Linkedin, Github, EnvelopeFill } from 'svelte-bootstrap-icons';
  import OSFLogo from '$lib/assets/logo-openstate.png';
  import exampleLogo from '$lib/assets/example-logo.png';
  import { IconHeart } from '@tabler/icons-svelte';
</script>

{#if $identity}
<div class="page">
  <ul>
    <li><a href="/archief/">Archief</a></li>
    <li>...</li>
  </ul>
</div>
{:else}
<p>Je bent momenteel niet ingelogt. Druk op de knop hieronder om naar de login pagina te gaan.</p>
<a href="//bron.live/login/" class="btn btn-primary">
Inloggen
</a>
{/if}
