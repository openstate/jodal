import {readable, writable} from "svelte/store";

export const apiDomainName = readable("api.bron.live");

export const identity = writable(null);
