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
    dateFrom: parseDateString(url.searchParams.get("van")),
    dateTo: parseDateString(url.searchParams.get("tot")),
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
  $effect(() => setParamsFromState("van", stringifyDate(state.dateFrom)));
  $effect(() => setParamsFromState("tot", stringifyDate(state.dateTo)));

  setContext("query", state);

  return state;
}

export const getQueryContext = () => getContext("query") as Query;

export type Query = ReturnType<typeof createQueryState>;

function parseDateString(dateString: string | null) {
  if (!dateString) return undefined;
  return new Date(dateString);
}

function stringifyDate(date: Date | undefined) {
  if (!date) return undefined;
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}
