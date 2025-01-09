import { fetchFeeds } from "$lib/loaders.js";

export async function load(event) {
  const feeds = await fetchFeeds(event);

  return { feeds };
}
