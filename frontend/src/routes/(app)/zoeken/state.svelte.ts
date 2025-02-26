import { goto } from "$app/navigation";
import { page } from "$app/state";
import { getContext, setContext } from "svelte";

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
    const oldURL = page.url;
    const newURL = new URL(oldURL);

    const encodedValue = typeof value === "string" ? value : value?.join(",");

    if (encodedValue === "" || !encodedValue) newURL.searchParams.delete(key);
    else newURL.searchParams.set(key, encodedValue);

    if (oldURL.search !== newURL.search) {
      goto(newURL.search === "" ? "?" : newURL.search, GOTO_PROPS);
      onChange?.();
    }
  };

  let state = $state(parseStateFromParams(page.url));

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
