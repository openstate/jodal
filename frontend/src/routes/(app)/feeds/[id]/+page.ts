import type { DocumentResponse, FeedResponse } from "$lib/types/api";
import { API_URL } from "$lib/api";

export async function load(event) {
  const feed: FeedResponse = await event
    .fetch(API_URL + `/feeds/${event.params.id}`, { credentials: "include" })
    .then((r) => r.json());

  let filters = [];

  console.log(feed);

  if (feed.locations.length > 0) {
    filters.push(`location.raw:${feed.locations.join(",")}`);
  }

  if (feed.sources.length > 0) {
    filters.push(`source:${feed.sources.join(",")}`);
  }

  const documents: Promise<DocumentResponse> = event
    .fetch(
      API_URL +
        `/documents/search?page=0&filter=${filters.join("|")}&published_to:now&sort=processed:desc,published:desc&limit=50&query=${feed.query}`,
    )
    .then((r) => r.json());

  return { documents, feed };
}
