import { API_URL } from "$lib/loaders";

export async function load({ fetch, url }) {
  const id = url.searchParams.get("id");
  const response = await fetch(API_URL + "/subscriptions/unsubscribe?user_id=" + id);
  return { success: response.ok };
}
