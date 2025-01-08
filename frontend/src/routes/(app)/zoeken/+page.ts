import { fetchAggregations, fetchDocuments, fetchLocations } from "./loaders";

export async function load(event) {
  const locations = await fetchLocations(event);
  const documents = fetchDocuments({ ...event, locations });
  const aggregations = fetchAggregations({ ...event, locations });

  return { documents, locations, aggregations };
}
