import { API_URL } from '$lib/api';
import type { Feed } from './types';

export async function load(event) {
  const response = await event.fetch(API_URL + `/columns`, {
    credentials: 'include',
  });

  if (!response.ok) return { feeds: null };

  const feeds: Feed[] = await response.json();

  return { feeds };
}
