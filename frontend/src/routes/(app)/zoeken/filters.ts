import type { LocationResponse } from "$lib/types/api";
import type { PageLoadEvent } from "./$types";
import { allSources } from "./sources";

export async function parseFilters(
  url: URL,
  locations: LocationResponse,
  include?: { sources?: boolean; organisations?: boolean },
) {
  let filters: Array<string> = [];

  let sources = url.searchParams.get("bronnen");
  if (!sources) sources = allSources.map((s) => s.value).join(",");
  if (!(include?.sources === false)) filters.push(`source:${sources}`);

  // The API does not currently support looking up documents by location type.
  // Therefore, we manually include each location matching a certain location type.
  let organisations = url.searchParams.get("organisaties");

  if (organisations?.includes("type:")) {
    organisations = organisations
      .split(",")
      .flatMap((org) => {
        if (org.startsWith("type:"))
          return locations.hits.hits.flatMap((loc) =>
            loc._source.type.includes(org.slice(5)) ? [loc._source.id] : [],
          );
        else return [org];
      })
      .join(",");
  }

  if (
    organisations &&
    !organisations.includes("*") &&
    !(include?.organisations === false)
  )
    filters.push(`location.raw:${organisations}`);

  let dateFrom = url.searchParams.get("van");
  if (dateFrom) filters.push(`processed_from:${dateFrom}`);

  let dateTo = url.searchParams.get("tot");
  if (dateTo) filters.push(`processed_to:${dateTo}`);

  return filters.join("|");
}
