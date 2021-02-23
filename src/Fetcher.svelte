<script>
import { onMount, onDestroy } from 'svelte';
import { get } from 'svelte/store';
import { identity, inquiries } from './stores.js';

onMount(function () {
  async function fetchColumns() {
    var url = 'http://api.jodal.nl/columns';
    return fetch(
      url, {credentials: "include"}).then(
        response => response.json()
      ).then(
        function (data) {
          console.log('Got columns:');
          console.dir(data);
          inquiries.set(data);
        }
      );
  }
  async function fetchIdentity() {
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
  fetchIdentity();
  fetchColumns();
});

onDestroy(function () {
});
</script>
