import type { Handle, HandleFetch, RequestEvent } from "@sveltejs/kit";
import type { Identity } from "$lib/stores";
import { API_URL } from "$lib/api";

async function getIdentity(event: RequestEvent) {
  const response = await event.fetch(API_URL + "/users/simple/me", {
    credentials: "include",
  });

  if (!response.ok) return null;
  return response.json() as Promise<Identity>;
}

// Intercepts all SvelteKit requests to retreive the user's session.
// See: https://svelte.dev/docs/kit/hooks#Server-hooks-handle
export const handle: Handle = async ({ event, resolve }) => {
  event.locals.identity = await getIdentity(event);

  const response = await resolve(event);

  return response;
};

// Intercepts all API calls on the server to include the user's session.
// See https://svelte.dev/docs/kit/hooks#Server-hooks-handle-fetch
export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
  if (
    request.url.replace(/https?:/, "").startsWith(API_URL) &&
    request.credentials !== "omit"
  )
    request.headers.set("cookie", event.request.headers.get("cookie") ?? "");

  return fetch(request);
};
