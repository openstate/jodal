import { identity, apiDomainName } from '$lib/stores';
import { get } from 'svelte/store';

export function initBronApp() {
  return getIdentity();
}

export function getIdentity() {
  console.log('should do identity check now!');
  var url = '//' + get(apiDomainName) + '/users/simple/me';
  return fetch(
    url, {credentials: "include", cache: 'no-cache'}).then(
      response => response.json()
    ).then(
      function (data) {
        if (data) {
          console.log('Identity: logged in as ', data);
          //console.dir(data);
          identity.set(data);
        } else {
          console.log('Identity: not logged in')
        }
        return data;
      }
    );
}
