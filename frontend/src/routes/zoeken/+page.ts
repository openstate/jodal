import type { DocumentResponse, LocationResponse } from '$lib/types/api.js';
import { API_URL, cacheFetch } from '$lib/api.js';
import type { PageLoadEvent } from './$types.js';

function fetchLocations({ fetch }: PageLoadEvent) {
  return cacheFetch<LocationResponse>('locations', () =>
    fetch(API_URL + `/locations/search?limit=500&sort=name.raw:asc`)
  );
}

async function fetchDocuments(
  { url, fetch }: PageLoadEvent,
  locationPromise: Promise<LocationResponse>
) {
  const query = url.searchParams.get('zoek');
  if (!query) return null;

  let organisations = url.searchParams.get('organisaties');

  // The API does not currently support looking up documents by location type.
  // Therefore, we manually include each location matching a certain location type.
  if (organisations?.includes('type:')) {
    const locations = await locationPromise;

    organisations = organisations
      .split(',')
      .flatMap((org) => {
        if (org.startsWith('type:'))
          return locations.hits.hits.flatMap((loc) =>
            loc._source.type.includes(org.slice(5)) ? [loc._source.id] : []
          );
        else return [org];
      })
      .join(',');
  }

  const filter = organisations && !organisations.includes("*") ? `location.raw:${organisations}` : '';

  const path = `/documents/search?query=${query}&filter=${filter}&sort=published:desc&page=0&limit=20`;

  return cacheFetch<DocumentResponse>(`documents:${url.search}`, () =>
    fetch(API_URL + path)
  );
}

export async function load(event) {
  const locationPromise = fetchLocations(event);
  const documentPromise = fetchDocuments(event, locationPromise);

  const [documents, locations] = await Promise.all([
    documentPromise,
    locationPromise,
  ]);

  return { documents, locations };
}
