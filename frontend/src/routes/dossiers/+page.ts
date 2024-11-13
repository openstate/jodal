import type { ElasticSearchResponse } from '$lib/types/elastic-search.js';

export async function load(event) {
  const search = event.url.searchParams.get("zoek");

  if (!search) return { documents: null };

  const response = await event.fetch(
    `//api.bron.live/documents/search?page=0&filter=|&published_to:now&sort=published:desc&limit=50&query=${search}`
  );

  if (!response.ok) return { documents: null };

  const documents = (await response.json()) as ElasticSearchResponse;

  return { documents };
}
