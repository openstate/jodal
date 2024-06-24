export const csr = true;
export const ssr = false;

import { error } from '@sveltejs/kit';
import { initBronApp } from '$lib/utils';
import { getAssets } from '$lib/asset';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
  const identity = await initBronApp();
  const assets = await getAssets();
  console.log('assets data load:', assets);
	return {assets};
}
