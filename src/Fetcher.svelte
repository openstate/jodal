<script>
import { onMount, onDestroy } from 'svelte';
import { get } from 'svelte/store';
import { identity } from './stores.js';

var url = 'http://api.jodal.nl/users/simple/me';
fetch(
  url,{credentials: "include"}).then(
    response => response.json()
  ).then(
    function (data) {
      console.log('Got identity in main:');
      console.dir(data);
      identity.set(data);
    }
  );

onMount(function () {
  async function fetchData() {
    var url = 'http://api.jodal.nl/users/simple/me';
    return fetch(
      url).then(
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
