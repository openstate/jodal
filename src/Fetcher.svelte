<script>
import { onMount, onDestroy } from 'svelte';
import { get } from 'svelte/store';
import { inquiries } from './stores.js';

var interval;

onMount(function () {
  async function fetchData() {
   console.log('should fetch data now!!');

   var all_inquiries = get(inquiries);
   var inquiry_index = Math.floor(Math.random() * all_inquiries.length);
   console.log('Should update inquiry ' + inquiry_index + ' now!');
   var default_new_entry = [{
     'key': "_3",
     'title': 'Raadscommissie Kunst Diversiteit en Democratisering',
     'type': 'Vergadering',
     'source': 'https://openbesluitvorming.nl/',
     'date': '11-11-2020',
     'time': '13:30'
   }];
 };
  interval = setInterval(fetchData, 5000);
  fetchData();
});

onDestroy(function () {
  clearInterval(interval);
});
</script>
