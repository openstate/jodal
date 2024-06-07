export const csr = true;
export const ssr = false;

import { error } from '@sveltejs/kit';
import { initBronApp } from '$lib/utils';

/** @type {import('./$types').PageLoad} */
export function load({ params }) {
    initBronApp();
}
