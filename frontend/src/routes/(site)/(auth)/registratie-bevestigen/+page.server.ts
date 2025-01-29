import { API_URL } from "$lib/loaders";

export async function load({ fetch, request }) {
  const id = new URL(request.url).searchParams.get("id");
  const response = await fetch(API_URL + "/users/verify?id=" + id);
  return { success: response.ok };
}
