import { readable, writable, get } from 'svelte/store';

export const drawerOpen = writable(false);
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

let default_entries = [
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

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array.map(function (i) {return i;});
}

export const inquiries = [
  writable({name: 'Amsterdam', order: 0, entries: shuffle(default_entries)}),
//  writable({name: 'Groningen', order: 1, entries: shuffle(default_entries)})
//  writable({name: 'Enschede', order: 2, entries: shuffle(default_entries)}),
//  writable({name: 'Leeuwarden', order: 3, entries: shuffle(default_entries)}),
//  writable({name: 'Roermond', order: 4, entries: shuffle(default_entries)}),
//  writable({name: 'Dordrecht', order: 5, entries: shuffle(default_entries)}),
//  writable({name: 'Middelburg', order: 6, entries: shuffle(default_entries)})
];

export function addInquiry(settings) {
  var max_order = Math.max.apply(Math, inquiries.map(function(i) { return get(i).order; }));
  var column_def = {
    ...settings,
    order: (max_order + 1),
    entries: shuffle(default_entries)
  };
  console.log('Pushing column:');
  console.dir(column_def);
  inquiries.push(writable(column_def));
  console.dir(inquiries);
}
