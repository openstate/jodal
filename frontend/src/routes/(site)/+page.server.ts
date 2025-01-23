import {  getRandomArticles } from "$lib/articles";
import { getRandomExamples } from "$lib/examples";
import { redirect } from "@sveltejs/kit";

export async function load(event) {
  if (event.locals.identity) throw redirect(307, "/zoeken");

  return { examples: getRandomExamples(), articles: await getRandomArticles() };
}
