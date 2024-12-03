import { API_URL } from '$lib/api';
import type { Actions } from '@sveltejs/kit';

export const actions = {
  default: async ({ fetch, request }) => {
    const formData = await request.formData();

    const response = await fetch(API_URL + '/columns', {
      credentials: 'include',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(formData)),
    });

    return { success: response.status };
  },
} satisfies Actions;
