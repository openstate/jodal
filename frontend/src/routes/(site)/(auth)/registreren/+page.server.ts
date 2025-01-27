import { fail, redirect, type Actions } from "@sveltejs/kit";
import { API_URL } from "$lib/loaders";

export function load({ locals }) {
  if (locals.identity) throw redirect(307, "/zoeken");
}

export const actions = {
  default: async ({ fetch, request }) => {
    const data = await request.formData();

    const response = await fetch(API_URL + "/users/register", {
      method: "POST",
      body: data,
    });

    if (!response.ok)
      return fail(400, {
        success: false,
        message: "Er is iets misgegaan. Probeer het opnieuw.",
      });

    return {
      success: true,
      message: "Check je e-mail om je registratie te bevestigen.",
    };
  },
} satisfies Actions;
