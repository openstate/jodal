import type { ElasticSearchResponse } from '$lib/types/elastic-search';
import type { Feed } from '../types';
import { API_URL } from '$lib/api';
import { error, fail } from '@sveltejs/kit';

export async function load(event) {
  const [query, id] = event.params.id.split('~');

  const searchPromise = event.fetch(
    API_URL +
      `/documents/search?page=0&filter=|&published_to:now&sort=published:desc&limit=50&query=${query}`
  );

  const feedPromise = event.fetch(API_URL + `/columns/${id}`, {
    credentials: 'include',
  });

  const [searchResponse, feedResponse] = await Promise.all([
    searchPromise,
    feedPromise,
  ]);

  if (!searchResponse.ok || !feedResponse.ok) error(400);

  const documents: ElasticSearchResponse = await searchResponse.json();
  const feed: Feed = await feedResponse.json();

  if (feed.user_query !== query) error(404);

  return { documents, feed };
}
