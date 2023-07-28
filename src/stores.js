import { readable, writable, get, derived } from 'svelte/store';
import { onMount } from "svelte";

export const domainName = 'jodal.nl';
export const apiDomainName = 'api.' + domainName;
export const testDomainName = 'test.' + domainName;

export const isTesting = readable((window.location.hostname == testDomainName));
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
  },
  {
    short: 'cvdr',
    name: 'Lokale wet- en regelgeving'
  }
]);

export const selected_inquiry_id = writable(null);
export const inquiries = writable([
//  {name: 'Amsterdam', locations:["GM0363"], user_query: "*", order: 0},
//  {name: 'Groningen', locations:["GM0014"], user_query: "*", order: 1}
]);

export const ordered_inquiries = derived(inquiries, $inquiries => [...$inquiries].sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0)));
export const selected_inquiry = derived(inquiries, $inquiries => [...$inquiries].filter(i => i.id == get(selected_inquiry_id)));

export function addInquiry(settings) {
  var inqs = get(inquiries);
  var max_order = (inqs.length > 0) ? Math.max.apply(Math, get(inquiries).map(function(i) { return i.order; })) : 0;
  var column_def = {
    ...settings,
    order: (max_order + 1)
  };

  if (get(isTesting)) {
    var column_def_update = {
      ...column_def,
      id: max_order + 1,
      date_end: null,
      date_start: null,
      sort: "published",
      sort_order: "desc",
      user_id: "x"
    };
    get(sources).forEach(function (s) {
      column_def_update['src_' + s.short] = true;
    });

    console.log('Anonymous column data:');
    console.dir(column_def_update);
    _addInquiry(column_def_update);
  } else {
    var url = window.location.protocol + '//' + apiDomainName + '/columns';
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
          _addInquiry(data);
        }
      );
    }
}

function _addInquiry(data) {
  console.log('Added column succesfully!:', data);
  //console.dir(data);
  var inqs = get(inquiries);
  inqs.push(data);
  inquiries.set(inqs);
  setTimeout(function() {
    document.getElementById('column-' + data.id).scrollIntoView();
  }, 100);
}

export function removeInquiry(column_id) {
  if (!get(isTesting)) {
    var url = window.location.protocol + '//' + apiDomainName + '/columns/' + column_id;
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
}
