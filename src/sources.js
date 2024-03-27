import { get } from 'svelte/store';
import { id2locations, apiDomainName, sources, locations } from './stores.js';

export function fetchSource(query, selected_sources, location_ids, date_start, date_end, sort_field, sort_order, stable, page, callback) {
  return fetchFromApi(query, selected_sources, location_ids.map(function (l) { return l.id;}), date_start, date_end, sort_field, sort_order, stable, page, callback);
}

function fetchFromApi(query, selected_sources, location_ids, date_start, date_end, sort_field, sort_order, stable, page, callback) {
  console.log('Should fetch locations ' + location_ids + ' using openspending now!');
  // 'http://api.jodal.nl/documents/search?query=*&filter=location.keyword:GM0777|GM0632&sort=published:desc'
  var api_filter = '&filter=';
  var current_sources = get(sources);
  if (selected_sources.length != current_sources.length) {
    api_filter += 'source:' + encodeURIComponent(selected_sources.join(","));
  }

  var all_locations = (location_ids.length <= 0) || (location_ids.includes('*'));
  if (!all_locations) {
    var loc_ids = location_ids;
    api_filter += '|location.raw:'+ location_ids.join(",");
  }

  if (stable !== null) {
    api_filter += "|published_to:" + encodeURIComponent(stable);
  }
  var date_filter = '';
  if (date_start) {
    date_filter = date_filter + '|published_from:' + encodeURIComponent(date_start);
  }
  if (date_end) {
    date_filter = date_filter + '|published_to:' + encodeURIComponent(date_end);
  } else {
    date_filter = date_filter + '|published_to:now';
  }
  console.log('date filter is now: ', date_filter);
  api_filter += date_filter;
  var url =  window.location.protocol + '//' + apiDomainName + '/documents/search?page='+ page + '&query=' + encodeURIComponent(query || '*') + api_filter +'&sort=' + sort_field + ':' + sort_order + '&limit=50';
  console.log(url);

  return fetch(
    url, {cache: 'no-cache'}).then(
      response => response.json()
    ).then(
      function (data) {
        var _id2locations = get(id2locations);
        //console.dir(data.hits.hits);
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
              doc_url: i._source.doc_url,
              url: i._source.url,
              data: i._source.data,
              _id: i._id,
              _index: i._index,
              _type: i._type,
              _score: i._score
            };
          });
        }
        callback(items, data);
      }
    );
}
