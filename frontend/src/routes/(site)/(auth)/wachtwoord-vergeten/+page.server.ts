import { fail, type Actions } from '@sveltejs/kit';
import { API_URL } from '$lib/api';

export const actions = {
  default: async ({ fetch, request }) => {
    const data = await request.formData();

    const response = await fetch(API_URL + '/users/forgot-password', {
      method: 'POST',
      body: data,
    });

    if (!response.ok)
      return fail(400, {
        success: false,
        message: 'Er is iets misgegaan. Probeer het opnieuw.',
      });

    return {
      success: true,
      message: 'Bevestigingsmail verstuurd.',
    };
  },
} satisfies Actions;
