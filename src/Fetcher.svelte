<script>
import { onMount, onDestroy } from 'svelte';
import { get } from 'svelte/store';
import { inquiries } from './stores.js';

var interval;

onMount(function () {
  async function fetchData() {
   //console.log('should fetch data now!!');

   // var idx = Math.floor(Math.random() * inquiries.length);
   // var inquiry;
   // const inquiry_unsubscribe = inquiries[idx].subscribe(v => inquiry = v);
   // //console.log('Should update inquiry ' + idx + ' now!');
   // var entry_idx = items.length + 10;
   // var default_new_entry = {
   //   'key': "_" + entry_idx,
   //   'title': 'Raadscommissie Kunst Diversiteit ' + entry_idx,
   //   'type': 'Vergadering',
   //   'source': 'https://openbesluitvorming.nl/',
   //   'date': '11-11-2020',
   //   'time': '13:30'
   // };
   // items.unshift(default_new_entry);
   // inquiries[idx].update(x => inquiry);
   // inquiry_unsubscribe();
   //all_inquiries[inquiry_index].entries.unshift(default_new_entry);
   //all_inquiries[inquiry_index].entries = [default_new_entry] + all_inquiries[inquiry_index].entries;
   //inquiries.set(all_inquiries);
 };
  interval = setInterval(fetchData, 5000);
  fetchData();
});

onDestroy(function () {
  clearInterval(interval);
});
</script>
