import type { DocumentResponse, LocationResponse } from "$lib/types/api";
import type { PageLoadEvent } from "./$types";
import { API_URL, cacheFetch } from "$lib/api";
import { parseFilters } from "./filters";

function fetchLocations({ fetch }: PageLoadEvent) {
  return cacheFetch<LocationResponse>("locations", () =>
    fetch(API_URL + `/locations/search?limit=500&sort=name.raw:asc`),
  );
}

async function fetchDocuments({
  url,
  locations,
  fetch = window.fetch,
}: {
  url: URL;
  locations: LocationResponse;
  fetch?: typeof window.fetch;
}) {
  const query = url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(url, locations);
  const path = `/documents/search?query=${query}&filter=${filter}&sort=processed:desc,published:desc&page=0&limit=20&default_operator=AND`;

  return cacheFetch<DocumentResponse>(`documents:${url.search}`, () =>
    fetch(API_URL + path),
  );
}

async function fetchAggregations(
  event: PageLoadEvent,
  locations: LocationResponse,
) {
  const query = event.url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(event.url, locations, { sources: false });
  const path = `/documents/search?query=${query}&filter=${filter}&sort=processed:desc,published:desc&limit=0&default_operator=AND`;

  return cacheFetch<DocumentResponse>(`aggregations:${query}:${filter}`, () =>
    event.fetch(API_URL + path),
  );
}

export async function load(event) {
  const locations = await fetchLocations(event);
  const documents = fetchDocuments({ ...event, locations });
  const aggregations = fetchAggregations(event, locations);

  return { documents, locations, aggregations };
}
