import { get } from 'svelte/store';
import { id2locations } from './stores.js';

export function fetchSource(query, source, location_ids, callback) {
  var source2func = {
    'poliflw': fetchPoliflw,
    'openspending': fetchOpenspending,
    'openbesluitvorming': fetchOpenBesluitVorming
  }

  if (location_ids.length <= 0) {
    console.log('not enough locations to warrant a fetch');
    return;
  }

  var fnc = source2func[source];
  if (typeof(fnc) !== 'undefined') {
    return fnc(query, location_ids, callback);
  }
}

function fetchOpenBesluitVorming(query, location_ids, callback) {
  _fetchOpenBesluitVorming(query, location_ids, ["AgendaItem", "Meeting"], "start_date", callback);
  _fetchOpenBesluitVorming(query, location_ids, ["MediaObject"], "last_discussed_at", callback);
}

function _fetchOpenBesluitVorming(query, location_ids, doc_types, date_field, callback) {
  console.log('Should fetch locations ' + location_ids + ' using openbesluitvorming now!');
  var types = {
    'MediaObject': 'Bestand',
    'AgendaItem': 'Agendapunt',
    'Report': 'Rapport',
    'Meeting': 'Vergadering',
    'Person': 'Persoon',
    'Membership': 'Lidmaatschap',
    'Organization': 'Organisatie',
    'ImageObject': 'Beeld'
  };
  var url = 'https://api.openraadsinformatie.nl/v1/elastic/_search';
  var ids_only = location_ids.map(function (l) { return l.replace('https://id.openraadsinformatie.nl/', '');});
  var range_filter = {};
  range_filter[date_field] = {"lte": "now"};
  var payload = {
    "aggs": {
      "types": {
        "terms": {
          "field": "@type.keyword"
        }
      }
    },
    "query": {
      "bool": {
        "must": [
          {
            "simple_query_string": {
                "query": query,
                "fields": ["name", "description", "text"]
            }
          }
        ],
        "filter": [
          {"terms": {"has_organization_name": ids_only}},
          {"terms": {"@type.keyword": doc_types}},
          {"range": range_filter}
        ]
      }
    },
    "highlight": {
      "fields": {
        "name": {},
        "description": {},
        "text": {}
      }
    },
    "_source": {
      "includes": [
        "*"
      ],
      "excludes": []
    },
    "size":10
  };
  var order = {};
  order[date_field] = {"order": "desc"};
  payload.sort = [order];
  return fetch(
    url, {
      method: 'POST',
      cache: 'no-cache',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify(payload)
    }).then(
      response => response.json()
    ).then(
      function (data) {
        var items = [];
        var _id2locations = get(id2locations);
        console.log('got obv data:');
        //console.dir(data);
        if (typeof(data.hits.hits) !== 'undefined') {
          // FIXME: i.meta.highlight.description is an array!
          items = data.hits.hits.map(function (i) {
            var desc;
            if (typeof(i.highlight) === 'undefined') {
              desc = '';
            } else {
              // TODO: can have more
              desc = i.highlight.name || i.highlight.description || i.highlight.text;
              if (typeof(desc) !== 'undefined') {
                desc = desc[0];
              }
            }
            var full_text = '';
            if (typeof(i._source.text_pages) !== 'undefined') {
              full_text = '<p>' + i._source.text_pages.map(function (p) {return p.text;}).join("</p><p>") + '</p>';
            } else {
              full_text = i._source.text;
            }
            var location = 'https://id.openraadsinformatie.nl/' + i._source.has_organization_name;
            return {
              key: i._source.start_date + '_' + i._id,
              date: i._source[date_field],
              title: i._source.name,
              highlight: desc,
              description: full_text || '',
              location: _id2locations[location],
              type: types[i._source["@type"]],
              source: 'openbesluitvorming',
              url: 'https://openbesluitvorming.nl/?zoekterm=' + encodeURIComponent(query) + '&organisaties=%5B%22' + i._index + '%22%5D&showResource=' + encodeURIComponent(encodeURIComponent('https://id.openraadsinformatie.nl/' + i._id))
            };
          });
        }
        callback(items);
      }
    );
}

function fetchOpenspending(query, location_ids, callback) {
  console.log('Should fetch locations ' + location_ids + ' using openspending now!');
  // 'http://api.jodal.nl/documents/search?query=*&filter=location.keyword:GM0777|GM0632&sort=published:desc'
  var url =  window.location.protocol + '//api.jodal.nl/documents/search?query=' + encodeURIComponent(query) + '&filter=source.keyword:openspending|location.keyword:'+ location_ids.join(",") +'&sort=published:desc';
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
            var desc = "";
            if (typeof(i._source.data.value) === 'undefined') {
              desc = i._source.description;
            } else {
              desc = i._source.data.value.toLocaleString('en-US', {
                style: 'currency',
                currency: 'EUR',
              }) + " in " + i._source.description;
            }
            return {
              key: i._source.published + "" + idx,
              date: i._source.published,
              title: i._source.title,
              highlight: desc,
              description: desc,
              location: _id2locations[i._source.location],
              type: i._source.type,
              source: 'openspending',
              url: i._source.url
            };
          });
        }
        callback(items);
      }
    );
}

function fetchPoliflw(query, location_ids, callback) {
  console.log('Should fetch locations ' + location_ids + ' using poliflw now!');
  // curl -s 'https://api.poliflw.nl/v0/search' -d '{"filters":{"location":{"terms":["Amsterdam"]}},"size":0}'
  var url = 'https://api.poliflw.nl/v0/search';
  var payload = {
    "query": query,
    "filters":{
      "location":{
        "terms": location_ids
      }
    },
    "sort": "date",
    "order": "desc",
    "size": 10
  };
  return fetch(
    url, {
      method: 'POST',
      cache: 'no-cache',
      body: JSON.stringify(payload)
    }).then(
      response => response.json()
    ).then(
      function (data) {
        var items = [];
        if (typeof(data.item) !== 'undefined') {
          // FIXME: i.meta.highlight.description is an array!
          items = data.item.map(function (i) {
            var desc = "";
            if (typeof(i.meta.highlight) === 'undefined') {
              if (typeof(i.description) !== 'undefined') {
                desc = i.description.substring(0,140) + '&hellip;';
              }
            } else {
              desc = i.meta.highlight.description;
            }
            return {
              key: i.date,
              date: i.date,
              title: i.title,
              highlight: desc,
              description: i.description,
              location: i.location,
              type: i.source,
              source: 'poliflw',
              url: 'https://poliflw.nl/l/' + i.location + '/' + i.parties[0] + '/' + i.id
            };
          });
        }
        callback(items);
      }
    );
}
