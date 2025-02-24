import { fetchAggregations, fetchLocations } from "$lib/loaders";

export async function load(event) {
  const organisationId = event.url.searchParams.get("organisatie");
  const locations = await fetchLocations(event);
  const aggregations = fetchAggregations({ ...event, organisationId, locations });
  return { locations, aggregations };
}
