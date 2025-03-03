import type {
  AggregationsResponse,
  DocumentResponse,
  FeedResponse,
  LocationResponse,
} from "$lib/types/api";
import { cacheFetch } from "$lib/fetch";
import { parseFilters, parseOrganisationFilters } from "./filters";
import type { LoadEvent } from "@sveltejs/kit";
import { createSearchQuery } from "./utils";

export const API_URL = "//api.bron.live" as const;

export function fetchLocations(event: Pick<LoadEvent, "fetch">) {
  return cacheFetch<LocationResponse>("locations", () =>
    event.fetch(API_URL + `/locations/search?limit=500&sort=name.raw:asc`),
  );
}

export function getLocationItems(
  locations: Awaited<ReturnType<typeof fetchLocations>>,
) {
  return locations.hits.hits
    .map((hit) => ({
      value: hit._source.id,
      label:
        hit._source.kind === "municipality" &&
        !hit._source.name.startsWith("Alle")
          ? `Gemeente ${hit._source.name}`
          : hit._source.name,
    }))
    .toSorted((a, b) => {
      const [allA, allB] = [a, b].map((i) => i.label.startsWith("Alle"));
      return Number(allB) - Number(allA);
    });
}

export async function fetchDocuments(
  event: Pick<LoadEvent, "fetch" | "url"> & {
    locations: LocationResponse;
    pageNumber?: number;
  },
) {
  event.pageNumber ??= 0;

  const query = event.url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(event.url, event.locations, {
    untilToday: query === "*",
  });

  const searchQuery = createSearchQuery({
    query,
    page: event.pageNumber ?? 0,
    limit: 20,
    filter,
    sort: "published:desc,processed:desc",
    default_operator: "AND",
  });

  return cacheFetch<DocumentResponse>(
    `documents:${event.url.search}:${event.pageNumber}`,
    () => event.fetch(API_URL + "/documents/search?" + searchQuery),
  );
}

export async function fetchDocument(
  event: Pick<LoadEvent, "fetch" | "params">,
) {
  const id = event.params.id;
  if (!id) return;

  return cacheFetch<DocumentResponse>(`document:${id}`, () =>
    event.fetch(API_URL + `/documents/search?query=id:${id}`),
  );
}

export async function fetchSearchAggregations(
  event: Pick<LoadEvent, "fetch" | "url"> & {
    locations: LocationResponse;
  },
) {
  const query = event.url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(event.url, event.locations, {
    sources: false,
  });

  const searchQuery = createSearchQuery({
    query,
    filter,
    limit: 0,
    default_operator: "AND",
  });

  return cacheFetch<DocumentResponse>(`aggregations:${query}:${filter}`, () =>
    event.fetch(API_URL + "/documents/search?" + searchQuery),
  );
}

export async function fetchAggregations(
  event: Pick<LoadEvent, "fetch"> & {
    organisationId: string | null;
    locations: LocationResponse;
  },
) {
  const organisationId = parseOrganisationFilters(
    event.organisationId,
    event.locations,
  );
  return cacheFetch<AggregationsResponse>(
    `aggregations:${event.organisationId ?? ""}`,
    () =>
      event.fetch(
        API_URL +
          `/documents/aggregations` +
          (organisationId && organisationId !== "*"
            ? `?organisation_id=${organisationId}`
            : ""),
      ),
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

  let filters = ["published_from:now-1w", "published_to:now+1d"];

  if (event.feed.locations.length > 0) {
    filters.push(`location.raw:${event.feed.locations.join(",")}`);
  }

  if (event.feed.sources.length > 0) {
    filters.push(`source:${event.feed.sources.join(",")}`);
  }

  const searchQuery = createSearchQuery({
    query: event.feed.query,
    limit: event.limit,
    filter: filters.join("|"),
    sort: "processed:desc,published:desc",
    default_operator: "AND",
  });

  const documents = cacheFetch<DocumentResponse>(
    `feed-documents:${event.feed.public_id}:${event.limit}`,
    () => event.fetch(API_URL + "/documents/search?" + searchQuery),
  );

  return documents;
}
