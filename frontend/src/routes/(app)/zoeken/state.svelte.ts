import { goto } from "$app/navigation";
import { page } from "$app/stores";
import { getContext, setContext } from "svelte";
import { get } from "svelte/store";

const GOTO_PROPS = {
  keepFocus: true,
  noScroll: true,
  replaceState: true,
  invalidateAll: true,
};

/** Creates a query state object that synchronizes with URL search parameters. */
export function createQueryState({ onChange }: { onChange?: () => void }) {
  const parseStateFromParams = (url: URL) => ({
    term: url.searchParams.get("zoek") ?? "",
    sources: url.searchParams.get("bronnen")?.split(",") ?? [],
    organisations: url.searchParams.get("organisaties")?.split(",") ?? [],
    dateFrom: url.searchParams.get("van") ?? undefined,
    dateTo: url.searchParams.get("tot") ?? undefined,
  });

  const setParamsFromState = (
    key: string,
    value: string | string[] | undefined,
  ) => {
    const url = get(page).url;
    const encodedValue = typeof value === "string" ? value : value?.join(",");

    if (encodedValue === "" || !encodedValue) url.searchParams.delete(key);
    else url.searchParams.set(key, encodedValue);

    goto(url.search === "" ? "?" : url.search, GOTO_PROPS);
    onChange?.();
  };

  let state = $state(parseStateFromParams(get(page).url));

  $effect(() => setParamsFromState("zoek", state.term));
  $effect(() => setParamsFromState("bronnen", state.sources));
  $effect(() => setParamsFromState("organisaties", state.organisations));
  $effect(() => setParamsFromState("van", state.dateFrom));
  $effect(() => setParamsFromState("tot", state.dateTo));

  setContext("query", state);

  return state;
}

export const getQueryContext = () => getContext("query") as Query;

export type Query = ReturnType<typeof createQueryState>;
