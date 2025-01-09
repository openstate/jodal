import { fetchFeed, fetchFeedDocuments } from "$lib/loaders";

export async function load(event) {
  const feed = await fetchFeed(event);
  const documents = fetchFeedDocuments({ ...event, feed });

  return { documents, feed };
}
