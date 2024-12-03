import type { LocationResponse } from "$lib/types/api";
import type { PageLoadEvent } from "./$types";
import { allSources } from "./sources";

export function composeFilters(sources: string[], organisations: string[]) {
  let filters: Array<string> = [""];

  if (sources.length < allSources.length && sources.length > 0)
    filters.push(`bronnen=${sources.join(",")}`);

  if (organisations.length > 0 && !organisations.includes("*"))
    filters.push(`organisaties=${organisations.join(",")}`);

  return filters.join("&");
}

export async function parseFilters(
  event: PageLoadEvent,
  locationPromise: Promise<LocationResponse>,
) {
  let filters: Array<string> = [];

  const sources = event.url.searchParams.get("bronnen");
  if (sources) filters.push(`source:${sources}`);

  // The API does not currently support looking up documents by location type.
  // Therefore, we manually include each location matching a certain location type.
  let organisations = event.url.searchParams.get("organisaties");

  if (organisations?.includes("type:")) {
    const locations = await locationPromise;

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

  if (organisations && !organisations.includes("*"))
    filters.push(`location.raw:${organisations}`);

  return filters.join("|");
}
