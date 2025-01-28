import { getRandomArticles } from "$lib/articles";
import { getRandomExamples } from "$lib/examples";

export async function load(event) {
  return { examples: getRandomExamples(), articles: await getRandomArticles() };
}
