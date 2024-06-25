import { apiDomainName } from '$lib/stores';
import { get } from 'svelte/store';
import { identity } from '$lib/stores';

export function createAsset(url, external_id) {
  var asset_url = '//' + get(apiDomainName) + '/assets';

  var params = {
    user_id: identity.sub,
    url: url,
    external_id: external_id
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

export function getAssets() {
  var asset_url = '//' + get(apiDomainName) + '/assets';

  var params = {
    user_id: identity.sub
    // more params?
  };

  return fetch(
    asset_url, {
      credentials: "include",
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(
      response => response.json()
    );
}
