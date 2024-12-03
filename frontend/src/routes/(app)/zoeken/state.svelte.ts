// const getSelectedOrganisations = () =>
//   $page.url.searchParams.get("organisaties")?.split(",") ?? [];

// const getSelectedSources = () =>
//   $page.url.searchParams.get("bronnen")?.split(",") ?? [];

// let queryInput = $state($page.url.searchParams.get("zoek") ?? "");
// let selectedOrganisations = $state(getSelectedOrganisations());
// let selectedSources = $state(getSelectedSources());

// $effect(() => {
//   queryInput = $page.url.searchParams.get("zoek") ?? "";
//   selectedOrganisations = getSelectedOrganisations();
//   selectedSources = getSelectedSources();
// });

export function createQueryState(url: URL) {
  let query = $state({
    term: url.searchParams.get("zoek") ?? "",
    sources: url.searchParams.get("bronnen")?.split(",") ?? [],
    organisations: url.searchParams.get("organisaties")?.split(",") ?? [],
  });

  $effect(() => {
    query = {
      term: url.searchParams.get("zoek") ?? "",
      sources: url.searchParams.get("bronnen")?.split(",") ?? [],
      organisations: url.searchParams.get("organisaties")?.split(",") ?? [],
    };
  });

  return query;
}
