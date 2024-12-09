import { API_URL } from '$lib/api';
import type { FeedResponse } from '$lib/types/api';

export async function load(event) {
  const response = await event.fetch(API_URL + `/feeds`, {
    credentials: 'include',
  });

  if (!response.ok) return { feeds: null };

  const feeds: FeedResponse[] = await response.json();

  return { feeds };
}
