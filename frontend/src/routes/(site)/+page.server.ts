import {  getRandomArticles } from "$lib/articles";
import { getRandomExamples } from "$lib/examples";
import { redirect } from "@sveltejs/kit";

export async function load(event) {
  return { examples: getRandomExamples(), articles: await getRandomArticles() };
}
