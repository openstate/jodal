import { fetchFeedDocuments, fetchFeeds } from "$lib/loaders.js";
import { redirect } from "@sveltejs/kit";

export async function load(event) {
  const { identity } = await event.parent();
  if (!identity) throw redirect(307, "/inloggen");

  const feeds = await fetchFeeds(event);

  return {
    feeds: feeds.map((feed) => ({
      ...feed,
      match: fetchFeedDocuments({ ...event, feed, limit: 1 }),
    })),
  };
}
