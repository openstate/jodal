import { page } from '$app/stores';
import { derived } from 'svelte/store';
import type { LocationResponse } from './types/api';

export type Identity = {
  applicationId: string;
  email: string;
  email_verified: boolean;
  family_name: string;
  given_name: string;
  roles: Array<string>;
  sub: string;
};

export const identity = derived(page, ($page) => $page.data?.identity);

export const locations = derived(page, ($page) => $page.data?.locations as LocationResponse | null);