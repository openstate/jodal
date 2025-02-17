import {
  fetchSearchAggregations,
  fetchDocuments,
  fetchLocations,
} from "$lib/loaders";

export async function load(event) {
  const locations = await fetchLocations(event);
  const documents = fetchDocuments({ ...event, locations });
  const aggregations = fetchSearchAggregations({ ...event, locations });

  return { documents, locations, aggregations };
}
