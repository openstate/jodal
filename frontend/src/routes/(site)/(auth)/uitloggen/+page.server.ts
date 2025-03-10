import { redirect, type Actions } from "@sveltejs/kit";
import { dev } from "$app/environment";

export const actions = {
  default: ({ cookies }) => {
    cookies.delete("session", {
      path: "/",
      secure: !dev,
      domain: "bron.live",
    });

    redirect(303, "/");
  },
} satisfies Actions;
