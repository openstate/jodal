import { fetchFeeds } from "$lib/loaders";

export async function load(event) {
  // These feeds are shown in navigation.
  const feeds = await fetchFeeds(event);

  return { feeds };
}
