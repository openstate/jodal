import { API_URL } from "$lib/loaders";
import { fail, redirect, type Actions } from "@sveltejs/kit";

export const actions = {
  delete: async ({ fetch, params, locals }) => {
    if (!locals.identity) throw redirect(307, "/inloggen");

    const response = await fetch(API_URL + `/feeds/${params.id}`, {
      method: "DELETE",
    });

    if (response.ok) throw redirect(307, "/feeds");

    return fail(response.status, { error: "Failed to delete feed" });
  },
} satisfies Actions;
