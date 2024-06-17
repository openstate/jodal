import { identity } from '$lib/stores';

export function initBronApp() {
  getIdentity();
}

export function getIdentity() {
  console.log('should do identity check now!');
  var apiDomainName = 'api.bron.live';
  var url = '//' + apiDomainName + '/users/simple/me';
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
      }
    );

}
