import { getArticle } from "$lib/articles";

export function load(event) {
  return getArticle(event.params.slug);
}
