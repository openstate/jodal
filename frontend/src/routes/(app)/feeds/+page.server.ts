import { API_URL } from "$lib/loaders";
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
        sources: data.getAll("sources"),
        locations: data.getAll("locations"),
      }),
    });

    const feed = await response.json();

    if (response.status === 401) {
      throw redirect(307, "/registreren");
    }

    throw redirect(307, `/feeds/${feed.public_id}`);
  },
} satisfies Actions;
