import type { DocumentResponse, LocationResponse } from "$lib/types/api";
import type { PageLoadEvent } from "./$types";
import { API_URL, cacheFetch } from "$lib/api";
import { parseFilters } from "./filters";

export function fetchLocations({
  fetch = window.fetch,
}: {
  fetch?: typeof window.fetch;
}) {
  return cacheFetch<LocationResponse>("locations", () =>
    fetch(API_URL + `/locations/search?limit=500&sort=name.raw:asc`),
  );
}

export async function fetchDocuments({
  url,
  locations,
  fetch = window.fetch,
  pageNumber = 0,
}: {
  url: URL;
  locations: LocationResponse;
  fetch?: typeof window.fetch;
  pageNumber?: number;
}) {
  const query = url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(url, locations);
  const path = `/documents/search?query=${query}&filter=${filter}&sort=processed:desc,published:desc&page=${pageNumber}&limit=20&default_operator=AND`;

  return cacheFetch<DocumentResponse>(`documents:${url.search}:${pageNumber}`, () =>
    fetch(API_URL + path),
  );
}

export async function fetchAggregations({
  url,
  locations,
  fetch = window.fetch,
}: {
  url: URL;
  locations: LocationResponse;
  fetch?: typeof window.fetch;
}) {
  const query = url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(url, locations, { sources: false });
  const path = `/documents/search?query=${query}&filter=${filter}&sort=processed:desc,published:desc&limit=0&default_operator=AND`;

  return cacheFetch<DocumentResponse>(`aggregations:${query}:${filter}`, () =>
    fetch(API_URL + path),
  );
}
