<script lang="ts">
  import { enhance } from '$app/forms';
  import { page } from '$app/stores';

  const userQuery = $page.url.searchParams.get('zoek') ?? '';

  let { data } = $props();
</script>

<h1>Feeds</h1>
<ul>
  {#each data.feeds ?? [] as feed}
    <li>
      <a href="/feeds/{feed.user_query}~{feed.id}">{feed.name}</a>
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
    name="user_query"
    placeholder="Zoekopdracht"
    required
    value={userQuery}
  />
  <input type="hidden" name="locations" value="*" />
  <input type="hidden" name="order" value="0" />
  <button type="submit" class="btn btn-primary">Aanmaken</button>
</form>
