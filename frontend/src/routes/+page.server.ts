import { getRandomExamples } from "$lib/examples";

export function load(e) {
  return { examples: !e.locals.identity ? getRandomExamples() : [] };
}
