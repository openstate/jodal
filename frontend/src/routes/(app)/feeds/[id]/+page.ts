import type { DocumentResponse, FeedResponse } from '$lib/types/api';
import { API_URL } from '$lib/api';
import { error } from '@sveltejs/kit';

export async function load(event) {
  const [enncoded_query, public_id] = event.params.id.split('~');
  const query = decodeURIComponent(enncoded_query);

  const searchPromise = event.fetch(
    API_URL +
      `/documents/search?page=0&filter=|&published_to:now&sort=published:desc&limit=50&query=${query}`
  );

  const feedPromise = event.fetch(API_URL + `/feeds/${public_id}`, {
    credentials: 'include',
  });

  const [searchResponse, feedResponse] = await Promise.all([
    searchPromise,
    feedPromise,
  ]);

  if (!searchResponse.ok || !feedResponse.ok) error(400);

  const documents: DocumentResponse = await searchResponse.json();
  const feed: FeedResponse = await feedResponse.json();

  if (feed.query !== query) error(404);

  return { documents, feed };
}
