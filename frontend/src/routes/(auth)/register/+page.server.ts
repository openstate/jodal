import { fail, type Actions } from '@sveltejs/kit';

export const actions = {
  default: async ({ fetch, request }) => {
    const data = await request.formData();

    const response = await fetch('//api.bron.live/users/register', {
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
      message: 'Check je e-mail om je registratie te bevestigen.',
    };
  },
} satisfies Actions;
