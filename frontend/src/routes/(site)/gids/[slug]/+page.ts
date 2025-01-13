import { marked } from "marked";

const articles = import.meta.glob("$lib/articles/*.md", {
  query: "?raw",
  import: "default",
});

export async function load(event) {
  const path = `/src/lib/articles/${event.params.slug}.md`;
  const markdown = await articles[path]();
  return { html: await marked.parse(markdown as string) };
}
