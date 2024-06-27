import { apiDomainName } from '$lib/stores';
import { get } from 'svelte/store';

export function warcDownloadURL(archive_id) {
  var url = '//' + get(apiDomainName) + '/archive/warc/download/' + archive_id;
  return url;
}
export function warcCreate(url) {
  console.log('shouldcreate warc now!');
  var url = '//' + get(apiDomainName) + '/archive/warc/create?' + new URLSearchParams({
    url: url
  });
  return fetch(
    url, {credentials: "include", cache: 'no-cache'}).then(
      response => response.json()
    ).then(
      function (data) {
        if (data) {
          console.log('warc creation response:  ', data);
          //console.dir(data);
          //identity.set(data);
        } else {
          console.log('warc could not be created');
        }
        return data;
      }
    );
}

export function warcStatus(archive_id) {
  console.log('shouldcreate warc now!');
  var url = '//' + get(apiDomainName) + '/archive/warc/' + archive_id;
  return fetch(
    url, {credentials: "include", cache: 'no-cache'}).then(
      response => response.json()
    ).then(
      function (data) {
        if (data) {
          console.log('warc status response:  ', data);
          //console.dir(data);
          //identity.set(data);
        } else {
          console.log('warc status was not gotten');
        }
        return data;
      }
    );
}

export function warcStatuses(archive_ids) {
  console.log('shouldcreate warc now!');
  var url = '//' + get(apiDomainName) + '/archive/warcs/' + archive_ids;
  return fetch(
    url, {credentials: "include", cache: 'no-cache'}).then(
      response => response.json()
    ).then(
      function (data) {
        if (data) {
          console.log('warc status response:  ', data);
          //console.dir(data);
          //identity.set(data);
        } else {
          console.log('warc status was not gotten');
        }
        return data;
      }
    );
}
