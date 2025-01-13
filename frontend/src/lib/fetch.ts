import { browser } from "$app/environment";
import { error } from "@sveltejs/kit";
import { LRUCache } from "lru-cache";

export const cache = new LRUCache({ max: 25 });

export const cacheFetch = async <T>(
  key: string,
  fetchCallback: () => ReturnType<typeof fetch>,
) => {
  if (browser && cache.has(key)) return cache.get(key) as T;

  const response = await fetchCallback();

  const result = await response.json();

  if (!response.ok) {
    console.error(key, response.status, result);
    throw error(response.status, result);
  }

  cache.set(key, result);

  return result as T;
};
