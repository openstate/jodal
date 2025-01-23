import fm from "front-matter";
import { marked } from "marked";

const glob = import.meta.glob("$lib/articles/*.md", {
  query: "?raw",
  import: "default",
});

export type Attributes = {
  title: string;
  description: string;
  image: string;
  feeds: string[];
  highlight: string;
};

export async function getArticle(slug: string) {
  const path = `/src/lib/articles/${slug}.md`;
  const markdown = await glob[path]();
  const { attributes, body } = fm<Attributes>(markdown as string);
  return { attributes, body: await marked.parse(body) };
}

export async function getArticles() {
  const paths = Object.keys(glob);
  return Promise.all(
    paths.map(async (path) => {
      const markdown = await glob[path]();
      const slug = path.split("/").pop()!.replace(".md", "");
      const { attributes } = fm<Attributes>(markdown as string);
      return { ...attributes, slug };
    }),
  );
}

export async function getRandomArticles() {
  const articles = await getArticles();
  return articles.sort(() => Math.random() - 0.5).slice(0, 3);
}

export type Articles = Awaited<ReturnType<typeof getArticles>>;
