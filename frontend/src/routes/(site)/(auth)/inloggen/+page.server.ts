import { dev } from '$app/environment';
import { fail, redirect, type Actions, type Cookies } from '@sveltejs/kit';
import { API_URL } from '$lib/loaders';

type SetCookie = Parameters<Cookies['set']>;

// Takes a response and returns a tuple that can be used in `cookies.set()`.
function getSessionCookie(response: Response, opts?: SetCookie[2]) {
  const setCookieHeader = response.headers.getSetCookie();
  if (!setCookieHeader[0]) throw new Error('No cookie header found');

  const cookie = setCookieHeader[0].split(';')[0];
  const splitCookie = cookie.split('=') as [string, string];

  const optsDefault = {
    path: '/',
    secure: !dev,
    maxAge: 60 * 60 * 24 * 7,
    domain: 'bron.live',
    ...opts,
  };

  return [...splitCookie, optsDefault] satisfies SetCookie;
}

export const actions = {
  default: async ({ fetch, request, cookies }) => {
    const data = await request.formData();

    const response = await fetch(API_URL + '/users/login', {
      method: 'POST',
      credentials: 'include',
      body: data,
    });

    if (!response.ok)
      return fail(400, {
        success: false,
        message: 'Er is iets misgegaan. Probeer het opnieuw.',
      });

    cookies.set(...getSessionCookie(response));

    redirect(307, '/');
  },
} satisfies Actions;
