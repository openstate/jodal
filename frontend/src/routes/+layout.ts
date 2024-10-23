export const ssr = false;

import { identity } from '$lib/stores';
import { getIdentity } from '$lib/utils';

export async function load(e) {
  identity.set(await getIdentity(e.fetch));
}
