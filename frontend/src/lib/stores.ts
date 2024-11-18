import { page } from '$app/stores';
import { derived, readable } from 'svelte/store';

export type Identity = {
  applicationId: string;
  email: string;
  email_verified: boolean;
  family_name: string;
  given_name: string;
  roles: Array<string>;
  sub: string;
};

export const identity = derived(page, ($page) => $page.data.identity);
