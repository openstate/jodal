import { API_URL } from "$lib/api";
import type { FeedResponse } from "$lib/types/api";

export async function load(event) {
  const feeds: Array<FeedResponse> = await event
    .fetch(API_URL + "/feeds", { credentials: "include" })
    .then((r) => r.json());

  return { feeds };
}
