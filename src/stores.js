import { readable, writable } from 'svelte/store';

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
export const inquiries = writable([
  {name: 'Amsterdam'},
  {name: 'Groningen'},
  {name: 'Enschede'},
  {name: 'Leeuwarden'},
  {name: 'Roermond'},
  {name: 'Dordrecht'},
  {name: 'Middelburg'},
]);
