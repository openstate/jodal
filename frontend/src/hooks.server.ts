import type { Handle, RequestEvent } from '@sveltejs/kit';
import type { Identity } from '$lib/stores';

async function getIdentity(event: RequestEvent) {
  const sessionCookie = event.cookies.get('session');
  if (!sessionCookie) return null;

  const response = await event.fetch('//api.bron.live/users/simple/me', {
    headers: { cookie: `session=${sessionCookie}` },
  });

  if (!response.ok) return null;

  return response.json() as Promise<Identity>;
}

// Intercepts all SvelteKit requests to retreive the user's session.
// See: https://svelte.dev/docs/kit/hooks
export const handle: Handle = async ({ event, resolve }) => {
  event.locals.identity = await getIdentity(event);

  const response = await resolve(event);

  return response;
};
