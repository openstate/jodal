import { fetchFeeds } from "$lib/loaders";

export async function load(event) {
  const { identity } = await event.parent();
  if (!identity) return { feeds: null };

  // These feeds are shown in navigation.
  const feeds = await fetchFeeds(event);

  return { feeds };
}
