export const csr = true;
export const ssr = false;

import { error } from '@sveltejs/kit';
import { initBronApp } from '$lib/utils';
import { getAssets } from '$lib/asset';
import { warcStatuses } from '$lib/archive';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
  const identity = await initBronApp();
  const assets = await getAssets();
  const external_ids = assets.map(function (a){return a.external_id;});
  console.log('assets data load:', assets);
  console.log('asset ext ids', external_ids);
  const statuses = await warcStatuses(external_ids.join(','));
  console.log('warc statuses:', statuses);
	return {assets};
}
