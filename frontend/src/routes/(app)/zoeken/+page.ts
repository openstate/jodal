import type { DocumentResponse, LocationResponse } from "$lib/types/api";
import type { PageLoadEvent } from "./$types";
import { API_URL, cacheFetch } from "$lib/api";
import { parseFilters } from "./filters";

function fetchLocations({ fetch }: PageLoadEvent) {
  return cacheFetch<LocationResponse>("locations", () =>
    fetch(API_URL + `/locations/search?limit=500&sort=name.raw:asc`),
  );
}

async function fetchDocuments(
  event: PageLoadEvent,
  locationPromise: Promise<LocationResponse>,
) {
  const query = event.url.searchParams.get("zoek") ?? "*";

  const filter = await parseFilters(event, locationPromise);
  const path = `/documents/search?query=${query}&filter=${filter}&sort=processed:desc,published:desc&page=0&limit=20&default_operator=AND`;

  return cacheFetch<DocumentResponse>(`documents:${event.url.search}`, () =>
    event.fetch(API_URL + path),
  );
}

export async function load(event) {
  const locations = fetchLocations(event);
  const documents = fetchDocuments(event, locations);


  return { documents, locations };
}
