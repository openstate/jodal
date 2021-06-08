import { get } from 'svelte/store';
import { id2locations } from './stores.js';

export function fetchSource(query, sources, location_ids, stable, page, callback) {
  return fetchFromApi(query, sources, location_ids.map(function (l) { return l.id;}), stable, page, callback);
}

function fetchFromApi(query, sources, location_ids, stable, page, callback) {
  console.log('Should fetch locations ' + location_ids + ' using openspending now!');
  // 'http://api.jodal.nl/documents/search?query=*&filter=location.keyword:GM0777|GM0632&sort=published:desc'
  var api_filter = '&filter=source.keyword:' + encodeURIComponent(sources.join(",")) + '|location.keyword:'+ location_ids.join(",")
  if (stable !== null) {
    api_filter += "|published_to:" + encodeURIComponent(stable);
  }
  var url =  window.location.protocol + '//api.jodal.nl/documents/search?page='+ page + '&query=' + encodeURIComponent(query) + api_filter +'&sort=published:desc&limit=50';
  console.log(url);

  return fetch(
    url, {cache: 'no-cache'}).then(
      response => response.json()
    ).then(
      function (data) {
        var _id2locations = get(id2locations);
        console.dir(data.hits.hits);
        var items = [];
        if (typeof(data.hits.hits) !== 'undefined') {
          // FIXME: i.meta.highlight.description is an array!
          var idx=0;
          items = data.hits.hits.map(function (i) {
            idx += 1;

            var hl;
            if (typeof(i.highlight) === 'undefined') {
              hl = '';
            } else {
              // TODO: can have more
              hl = i.highlight.title || i.highlight.description;
              if (typeof(hl) !== 'undefined') {
                hl = hl[0];
              }
            }


            var desc = i._source.description;

            // TODO: refactor this into something neater
            if (i._source.source == 'openspending') {
              if (typeof(i._source.data.value) === 'undefined') {
                desc = i._source.description;
              } else {
                desc = i._source.data.value.toLocaleString('en-US', {
                  style: 'currency',
                  currency: 'EUR',
                }) + " in " + i._source.description;
              }
              hl = desc;
            }

            return {
              key: i._source.published + "" + idx,
              date: i._source.published,
              title: i._source.title,
              highlight: hl || '',
              description: desc,
              location: _id2locations[i._source.location],
              type: i._source.type,
              source: i._source.source,
              url: i._source.url,
              data: i._source.data,
              _id: i._id,
              _index: i._index,
              _type: i._type
            };
          });
        }
        callback(items, data);
      }
    );
}
