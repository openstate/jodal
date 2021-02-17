<script>
import { onMount, onDestroy } from 'svelte';
import { get } from 'svelte/store';
import { identity } from './stores.js';

onMount(function () {
  async function fetchData() {
    var url = 'http://api.jodal.nl/users/simple/me';
    return fetch(
      url, {credentials: "include"}).then(
        response => response.json()
      ).then(
        function (data) {
          console.log('Got identity:');
          console.dir(data);
          identity.set(data);
        }
      );
  };
  fetchData();
});

onDestroy(function () {
});
</script>
