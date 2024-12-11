import { goto } from "$app/navigation";
import { page } from "$app/stores";
import { get } from "svelte/store";

const GOTO_PROPS = {
  keepFocus: true,
  noScroll: true,
  replaceState: true,
  invalidateAll: true,
}

/** Creates a query state object that synchronizes with URL search parameters. */
export function createQueryState() {
  const parseStateFromParams = (url: URL) => ({
    term: url.searchParams.get("zoek") ?? "",
    sources: url.searchParams.get("bronnen")?.split(",") ?? [],
    organisations: url.searchParams.get("organisaties")?.split(",") ?? [],
  });

  const setParamsFromState = (key: string, value: string | string[]) => {
    const url = get(page).url;
    const encodedValue = typeof value === "string" ? value : value.join(",");

    if (encodedValue === "") url.searchParams.delete(key);
    else url.searchParams.set(key, encodedValue);

    goto(url.search === "" ? "?" : url.search, GOTO_PROPS);
  };

  let state = $state(parseStateFromParams(get(page).url));

  $effect(() => setParamsFromState("zoek", state.term));
  $effect(() => setParamsFromState("bronnen", state.sources));
  $effect(() => setParamsFromState("organisaties", state.organisations));

  return state;
}

export type Query = ReturnType<typeof createQueryState>;
