<script lang="ts">
  import { enhance } from "$app/forms";
  import { page } from "$app/stores";

  const userQuery = $page.url.searchParams.get("zoek") ?? "";

  let { data } = $props();
</script>

<h1>Feeds</h1>
<ul>
  {#each data.feeds ?? [] as feed}
    <li>
      <a href="/feeds/{encodeURIComponent(feed.query)}~{feed.public_id}">{feed.name}</a>
    </li>
  {:else}
    <p>Geen feeds gevonden.</p>
  {/each}
</ul>

<h2>Nieuwe feed</h2>
<form method="POST" use:enhance>
  <input type="text" name="name" placeholder="Naam" required />
  <input
    type="text"
    name="query"
    placeholder="Zoekopdracht"
    required
    value={userQuery}
  />
  <input type="hidden" name="locations" value="" />
  <input type="hidden" name="sources" value="" />
  <button type="submit" class="btn btn-primary">Aanmaken</button>
</form>
