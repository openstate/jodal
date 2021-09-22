import { readable, writable, get, derived } from 'svelte/store';
import { onMount } from "svelte";

export const isTesting = readable((window.location.hostname == 'test.jodal.nl'));
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

export const ordered_inquiries = derived(inquiries, $inquiries => [...$inquiries].sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0)));

export function addInquiry(settings) {
  var inqs = get(inquiries);
  var max_order = Math.max.apply(Math, inqs.map(function(i) { return i.order; }));
  var column_def = {
    ...settings,
    order: (max_order + 1)
  };

  var url = window.location.protocol + '//api.jodal.nl/columns';
  return fetch(
    url, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(column_def),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(
      response => response.json()
    ).then(
      function (data) {
        console.log('Added column succesfully!:', data);
        //console.dir(data);
        inqs.push(data);
        inquiries.set(inqs);
        setTimeout(function() {
          document.getElementById('column-' + data.id).scrollIntoView();
        }, 100);
      }
    );
}

export function removeInquiry(column_id) {
  var url = window.location.protocol + '//api.jodal.nl/columns/' + column_id;
  return fetch(
    url, {
      method: "DELETE",
      credentials: "include",
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(
      function (data) {
        console.log('Deleted column ' + column_id + ' succesfully!:');
        // var inqs = get(inquiries).filter(function (i) {return i.id != column_id;});
        // console.log('inquiries after deletion:');
        // console.dir(inqs);
        // inquiries.set(inqs);
      }
    );
}
