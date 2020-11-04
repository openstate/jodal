import { writable } from 'svelte/store';

export const drawerOpen = writable(false);
export const inquiries = writable([
  {name: 'Amsterdam'},
  {name: 'Groningen'},
  {name: 'Enschede'},
  {name: 'Leeuwarden'},
  {name: 'Roermond'},
  {name: 'Dordrecht'},
  {name: 'Middelburg'},
]);
