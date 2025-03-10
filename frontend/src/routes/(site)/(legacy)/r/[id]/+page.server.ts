import { fetchDocument } from "$lib/loaders";
import { error, redirect } from "@sveltejs/kit";

export async function load(event) {
  const data = await fetchDocument(event);
  if (!data) error(404);

  const source = data.hits.hits[0]._source;
  const url =
    source.source == "openbesluitvorming" ? source.doc_url : source.url;

  redirect(308, url);
}
