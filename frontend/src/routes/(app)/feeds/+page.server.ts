import { API_URL } from "$lib/api";
import { redirect, type Actions } from "@sveltejs/kit";

export const actions = {
  default: async ({ fetch, request }) => {
    const data = await request.formData();

    const response = await fetch(API_URL + "/feeds", {
      credentials: "include",
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: data.get("name"),
        query: data.get("query"),
        sources: data.get("sources"),
        locations: data.get("locations"),
      }),
    });

    const feed = await response.json();

    throw redirect(307, `/feeds/${feed.public_id}`);
  },
} satisfies Actions;
