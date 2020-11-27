import { readable, writable, get } from 'svelte/store';
import { onMount } from "svelte";

export const drawerOpen = writable(false);

export const locations = writable([]);

export const sources = readable([
  {
    short: 'obv',
    name: 'Open Besluitvorming'
  },
  {
    short: 'poliflw',
    name: 'Poliflw'
  }
]);

export let default_entries = [
  {
    'key': "_3",
    'title': 'Raadscommissie Kunst Diversiteit en Democratisering',
    'type': 'Vergadering',
    'source': 'https://openbesluitvorming.nl/',
    'date': '11-11-2020',
    'time': '13:30'
  },
  {
    'key': "_2",
    'title': 'Deze vergadering vindt digitaal plaats. Insprekers kunnen digitaal inspreken',
    'type': 'Agendapunt',
    'source': 'https://openbesluitvorming.nl/',
    'date': '11-11-2020',
    'time': '12:45'
  },
  {
    'key': "_3",
    'title': 'Commissie Agenda (Definitieve)',
    'type': 'Document',
    'source': 'https://openbesluitvorming.nl/',
    'date': '11-11-2020',
    'time': '12:45'
  },
  {
    'key': "_4",
    'title': 'Vergadering 26-07-2020'
  },
  {
    'key': "_5",
    'title': 'Vergadering 26-06-2020'
  },
  {
    'key': "_6",
    'title': 'Vergadering 26-05-2020'
  },
  {
    'key': "_7",
    'title': 'Vergadering 26-04-2020'
  }
];

export const inquiries = writable([
  {name: 'Amsterdam', order: 0},
  {name: 'Groningen', order: 1}
//  writable({name: 'Enschede', order: 2, entries: shuffle(default_entries)}),
//  writable({name: 'Leeuwarden', order: 3, entries: shuffle(default_entries)}),
//  writable({name: 'Roermond', order: 4, entries: shuffle(default_entries)}),
//  writable({name: 'Dordrecht', order: 5, entries: shuffle(default_entries)}),
//  writable({name: 'Middelburg', order: 6, entries: shuffle(default_entries)})
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
