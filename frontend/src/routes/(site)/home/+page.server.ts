import { getRandomExamples } from "$lib/examples";

export function load() {
  return { examples: getRandomExamples() };
}
