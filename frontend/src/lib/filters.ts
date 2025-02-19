import type { LocationResponse } from "$lib/types/api";
import { allSources } from "./sources";

export function parseOrganisationFilters(
  organisations: string | null,
  locations: LocationResponse,
) {
  if (organisations?.includes("type:"))
    return organisations
      .split(",")
      .flatMap((org) => {
        if (org.startsWith("type:"))
          return locations.hits.hits.flatMap((loc) =>
            loc._source.type.includes(org.slice(5)) ? [loc._source.id] : [],
          );
        else return [org];
      })
      .join(",");

  return organisations;
}

export async function parseFilters(
  url: URL,
  locations: LocationResponse,
  include?: {
    sources?: boolean;
    organisations?: boolean;
    untilToday?: boolean;
  },
) {
  let filters: Array<string> = [];

  let sources = url.searchParams.get("bronnen");
  if (!sources) sources = allSources.map((s) => s.value).join(",");
  if (!(include?.sources === false)) filters.push(`source:${sources}`);

  // The API does not currently support looking up documents by location type.
  // Therefore, we manually include each location matching a certain location type.
  let organisations = parseOrganisationFilters(
    url.searchParams.get("organisaties"),
    locations,
  );

  if (
    organisations &&
    !organisations.includes("*") &&
    !(include?.organisations === false)
  )
    filters.push(`location.raw:${organisations}`);

  let dateFrom = url.searchParams.get("van");
  if (dateFrom) filters.push(`published_from:${dateFrom}`);

  let dateTo = url.searchParams.get("tot");
  if (dateTo) filters.push(`published_to:${dateTo}`);
  else if (include?.untilToday)
    filters.push(`published_to:${new Date().toISOString().split("T")[0]}`);

  return filters.join("|");
}
