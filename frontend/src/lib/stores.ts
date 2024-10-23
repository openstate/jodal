import { readable, writable } from 'svelte/store';

export const apiDomainName = readable('api.bron.live');

export type Identity = {
  applicationId: string;
  email: string;
  email_verified: boolean;
  family_name: string;
  given_name: string;
  roles: Array<string>;
  sub: string;
};

export const identity = writable<Identity>(null);
