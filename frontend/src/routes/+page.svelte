<script lang="ts">
  /** The front-end is divided into two main parts, denoted by the `(site)` and `(app)` route groups. The `(site)` route group is responsible for the public-facing website, while the `(app)` route group is responsible for the application itself. This route (with path `/`) displays either the landing page defined in `/(site)/home` or the app home page `/(app)/app`, depending on the user's session. */

  import AppLayout from "./(app)/+layout.svelte";
  import AppPage from "./(app)/app/+page.svelte";
  import SiteLayout from "./(site)/+layout.svelte";
  import SitePage from "./(site)/home/+page.svelte";

  let { data } = $props();
</script>

{#if data.identity}
  <AppLayout {data}>
    <AppPage {data} />
  </AppLayout>
{:else}
  <SiteLayout>
    <SitePage {data} />
  </SiteLayout>
{/if}
