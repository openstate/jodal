import { API_URL } from "$lib/loaders";
import { redirect, type Actions } from "@sveltejs/kit";

const getFormArray = (data: FormData, key: string) => {
  const value = data.get(key);
  if (typeof value !== "string") return [];
  return value.split(",").filter((item) => item !== "");
};

export const actions = {
  default: async ({ fetch, request, locals }) => {
    if (!locals.identity) throw redirect(307, "/registreren");

    const data = await request.formData();

    let frequency = data.get("frequency");
    if (frequency === "IMMEDIATE") frequency = "";

    const body = JSON.stringify({
      name: data.get("name"),
      query: data.get("query"),
      sources: getFormArray(data, "sources"),
      locations: getFormArray(data, "locations"),
      frequency,
    });

    const response = await fetch(API_URL + "/feeds", {
      credentials: "include",
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
    });

    if (response.status === 401) {
      throw redirect(307, "/registreren");
    }

    const feed = await response.json();

    throw redirect(307, `/feeds/${feed.public_id}`);
  },
} satisfies Actions;
