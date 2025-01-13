import { fetchFeedDocuments, fetchFeeds } from "$lib/loaders.js";

export async function load(event) {
  const feeds = await fetchFeeds(event);

  return {
    feeds: feeds.map((feed) => ({
      ...feed,
      match: fetchFeedDocuments({ ...event, feed, limit: 1 }),
    })),
  };
}
