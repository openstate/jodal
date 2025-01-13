import type {
  DocumentResponse,
  FeedResponse,
  LocationResponse,
} from "$lib/types/api";
import { cacheFetch } from "$lib/fetch";
import { parseFilters } from "./filters";
import type { LoadEvent } from "@sveltejs/kit";

export const API_URL = "//api.bron.live" as const;

export function fetchLocations(event: Pick<LoadEvent, "fetch">) {
  return cacheFetch<LocationResponse>("locations", () =>
    event.fetch(API_URL + `/locations/search?limit=500&sort=name.raw:asc`),
  );
}

export async function fetchDocuments(
  event: Pick<LoadEvent, "fetch" | "url"> & {
    locations: LocationResponse;
    pageNumber?: number;
  },
) {
  event.pageNumber ??= 0;

  const query = event.url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(event.url, event.locations);
  const path = `/documents/search?query=${query}&filter=${filter}&sort=processed:desc,published:desc&page=${event.pageNumber}&limit=20&default_operator=AND`;

  console.log(API_URL + path);

  return cacheFetch<DocumentResponse>(
    `documents:${event.url.search}:${event.pageNumber}`,
    () => event.fetch(API_URL + path),
  );
}

export async function fetchAggregations(
  event: Pick<LoadEvent, "fetch" | "url"> & {
    locations: LocationResponse;
  },
) {
  const query = event.url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(event.url, event.locations, {
    sources: false,
  });
  const path = `/documents/search?query=${query}&filter=${filter}&sort=processed:desc,published:desc&limit=0&default_operator=AND`;

  return cacheFetch<DocumentResponse>(`aggregations:${query}:${filter}`, () =>
    event.fetch(API_URL + path),
  );
}

export async function fetchFeeds(event: Pick<LoadEvent, "fetch">) {
  const feeds = cacheFetch<FeedResponse[]>("feeds", () =>
    event.fetch(API_URL + `/feeds`, {
      credentials: "include",
    }),
  );

  return feeds;
}

export async function fetchFeed(event: Pick<LoadEvent, "params" | "fetch">) {
  const feed = cacheFetch<FeedResponse>(`feed:${event.params.id}`, () =>
    event.fetch(API_URL + `/feeds/${event.params.id}`, {
      credentials: "include",
    }),
  );

  return feed;
}

export async function fetchFeedDocuments(
  event: Pick<LoadEvent, "fetch"> & { feed: FeedResponse; limit?: number },
) {
  event.limit ??= 50;

  let filters = [];

  if (event.feed.locations.length > 0) {
    filters.push(`location.raw:${event.feed.locations.join(",")}`);
  }

  if (event.feed.sources.length > 0) {
    filters.push(`source:${event.feed.sources.join(",")}`);
  }

  const documents = cacheFetch<DocumentResponse>(
    `feed-documents:${event.feed.public_id}:${event.limit}`,
    () =>
      event.fetch(
        API_URL +
          `/documents/search?page=0&filter=${filters.join("|")}&published_to:now&sort=processed:desc,published:desc&limit=${event.limit}&query=${event.feed.query}`,
      ),
  );

  return documents;
}
