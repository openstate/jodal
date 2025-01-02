import { API_URL } from "$lib/api";
import type { FeedResponse } from "$lib/types/api";

export async function load(event) {
  if (!event.data.identity) return { ...event.data, feeds: null };

  const feeds: Array<FeedResponse> = await event
    .fetch(API_URL + "/feeds", { credentials: "include" })
    .then((r) => r.json());

  return { ...event.data, feeds };
}
