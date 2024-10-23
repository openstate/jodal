import { dev } from '$app/environment';
import { identity, type Identity } from '$lib/stores';

const baseURL = dev ? 'http://api.bron.live' : 'https://api.bron.live';

type Fetch = (
  input: RequestInfo | URL,
  init?: RequestInit
) => Promise<Response>;

export function getIdentity(fetch: Fetch = window.fetch): Promise<Identity> {
  return fetch(baseURL + '/users/simple/me', {
    credentials: 'include',
    cache: 'no-cache',
  }).then((response) => response.json());
}

export function logout() {
  return fetch(baseURL + '/users/logout', {
    credentials: 'include',
    method: 'POST',
  }).then(async (response) => {
    if (response.ok && 'success' in (await response.json())) {
      identity.set(null);
    }
  });
}
