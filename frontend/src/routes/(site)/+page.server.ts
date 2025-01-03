import { getRandomExamples } from "$lib/examples";
import { redirect } from "@sveltejs/kit";

export function load(event) {
  if (event.locals.identity) throw redirect(307, "/app");

  return { examples: getRandomExamples() };
}
