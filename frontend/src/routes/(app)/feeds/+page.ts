import { fetchFeedDocuments, fetchFeeds } from "$lib/loaders";
import { redirect } from "@sveltejs/kit";

export async function load(event) {
  const { identity } = await event.parent();
  if (!identity) throw redirect(307, "/registreren");

  const feeds = await fetchFeeds(event);

  return {
    feeds: feeds.map((feed) => ({
      ...feed,
      match: fetchFeedDocuments({ ...event, feed, limit: 1 }),
    })),
  };
}
