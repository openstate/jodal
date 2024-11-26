import { browser } from '$app/environment';
import { error } from '@sveltejs/kit';

export const API_URL = '//api.bron.live' as const;

export const cache = new Map<string, string>();

export const cacheFetch = async <T>(
  key: string,
  fetchCallback: () => ReturnType<typeof fetch>
) => {
  if (browser && cache.has(key)) return cache.get(key) as T;

  const response = await fetchCallback();

  const result = await response.json();

  if (!response.ok) throw error(response.status, result);

  cache.set(key, result);

  return result as T;
};
