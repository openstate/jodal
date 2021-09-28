<script>
import { onMount, onDestroy } from 'svelte';
import { get } from 'svelte/store';
import { identity, inquiries, locations, id2locations, fetchingEnabled, isTesting } from './stores.js';

onMount(function () {
  async function fetchColumns() {
    if (!get(isTesting)) {
      var url = window.location.protocol + '//api.jodal.nl/columns';
      return fetch(
        url, {credentials: "include", cache: 'no-cache'}).then(
          response => response.json()
        ).then(
          function (data) {
            if ((typeof(data) === 'object') && (data.length)) {
              console.log('Got columns:');
              //console.dir(data);
              inquiries.set(data);
            }
          }
        );
    }
  }
  async function fetchIdentity() {
    if (!get(isTesting)) {
      var url = window.location.protocol + '//api.jodal.nl/users/simple/me';
      return fetch(
        url, {credentials: "include", cache: 'no-cache'}).then(
          response => response.json()
        ).then(
          function (data) {
            if (data) {
              console.log('Got identity:');
              //console.dir(data);
              identity.set(data);
            }
          }
        );
    }
  };
  async function fetchLocations() {
    return fetch(window.location.protocol + '//api.jodal.nl/locations/search?limit=500&sort=name.keyword:asc')
      .then(r => r.json())
      .then(data => {
        console.log('got locations data:')
        console.log(data);
        var items = data.hits.hits.map(function (l) {
          return l._source;
        })
        var _id2locations = {};
        items.forEach(function (i) {
          i['sources'].forEach(function (s) {
            _id2locations[s['id']] = i['name']
          })
        })
        console.dir('id2locations:')
        //console.log(_id2locations);
        id2locations.set(_id2locations);
        console.log('location items:')
        //console.dir(items)
        locations.set(items);
        console.log('selectable locations:')
        //console.dir($selectable_locations)
        console.log('setting fetching to enabled!')
        fetchingEnabled.set(true)
      });
  };
  fetchIdentity();
  fetchColumns();
  fetchLocations();
});

onDestroy(function () {
});
</script>
