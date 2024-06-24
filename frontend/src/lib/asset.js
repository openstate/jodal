import { apiDomainName } from '$lib/stores';
import { get } from 'svelte/store';
import { identity } from '$lib/stores';

export function createAsset(url) {
  var asset_url = '//' + get(apiDomainName) + '/assets';

  var params = {
    user_id: identity.sub,
    url: url
    // more params?
  };

  return fetch(
    asset_url, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(params),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(
      response => response.json()
    );
}
