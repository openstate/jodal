import { fetchAggregations } from "$lib/loaders";

export async function load(event) {
  const organisationId = event.url.searchParams.get("organisatie");
  const aggregations = fetchAggregations({ ...event, organisationId });
  return { aggregations };
}
