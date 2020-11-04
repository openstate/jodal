<script>
import { onMount, onDestroy } from 'svelte';

var interval;

onMount(function () {
  async function fetchData() {
   console.log('should fetch data now!!');
  }

  interval = setInterval(fetchData, 5000);
  fetchData();
});

onDestroy(function () {
  clearInterval(interval);
});
</script>
