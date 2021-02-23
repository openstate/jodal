import { readable, writable, get, derived } from 'svelte/store';
import { onMount } from "svelte";

export const identity = writable(false);

export const fetchingEnabled = writable(false);

export const drawerOpen = writable(false);

export const locations = writable([]);
export const id2locations = writable({});
export const selectable_locations = derived(locations, $locations => Object.values($locations).map(function (l) { return {value: l.id, label: l.name}}))
export const sources = readable([
  {
    short: 'openbesluitvorming',
    name: 'Open Besluitvorming'
  },
  {
    short: 'poliflw',
    name: 'Poliflw'
  },
  {
    short: 'openspending',
    name: 'Openspending'
  }
]);

export const inquiries = writable([
//  {name: 'Amsterdam', locations:["GM0363"], user_query: "*", order: 0},
//  {name: 'Groningen', locations:["GM0014"], user_query: "*", order: 1}
]);

export function addInquiry(settings) {
  var inqs = get(inquiries);
  var max_order = Math.max.apply(Math, inqs.map(function(i) { return i.order; }));
  var column_def = {
    ...settings,
    order: (max_order + 1)
  };
  inqs.push(column_def);
  inquiries.set(inqs);
}
