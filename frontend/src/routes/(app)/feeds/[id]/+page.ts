import { fetchFeed, fetchFeedDocuments } from "$lib/loaders";
import { redirect } from "@sveltejs/kit";

export async function load(event) {
  const { identity } = await event.parent();
  if (!identity) redirect(303, "/inloggen");

  const feed = await fetchFeed(event);
  const documents = fetchFeedDocuments({ ...event, feed });

  return { documents, feed };
}
