import { getArticles } from "$lib/articles.js";
import { fetchFeeds } from "$lib/loaders";

export async function load(event) {
  const { identity } = await event.parent();
  const articles = await getArticles();

  if (!identity) return { feeds: null, articles };

  const feeds = await fetchFeeds(event);

  return { feeds, articles };
}
