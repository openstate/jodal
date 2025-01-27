import about from "./about.md?raw";
import { marked } from "marked";

export async function load() {
  let markdown = await marked.parse(about);
  const headings: Array<{ id: string; text: string }> = [];

  // Replace headings and collect h2s
  markdown = markdown.replace(
    /<h([1-6])>(.+?)<\/h[1-6]>/g,
    (_, level, text) => {
      const id = `heading-${text
        .toLowerCase()
        .replace(/[^\w\s-]/g, "")
        .replace(/\s+/g, "-")}`;

      if (level === "2") headings.push({ id, text });

      return `<h${level} id="${id}">${text}</h${level}>`;
    },
  );

  return { markdown, headings };
}
