import { get } from 'svelte/store';
import { id2locations } from './stores.js';

export function fetchSource(query, source, location_ids, callback) {
  var source2func = {
    'poliflw': fetchPoliflw,
    'openspending': fetchOpenspending,
    'openspendinglabels': fetchOpenspendingLabels,
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
          {"terms": {"@type.keyword": ["MediaObject", "AgendaItem", "Meeting"]}},
          {"range": {"start_date": {"lte": "now"}}}
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
    "sort": [
      {"start_date": {"order": "desc"}}
    ],
    "size":10
  };
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
            var location = 'https://id.openraadsinformatie.nl/' + i._source.has_organization_name;
            return {
              key: i._source.start_date,
              date: i._source.start_date,
              title: i._source.name,
              description: desc,
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

function fetchOpenspendingLabels(query, location_ids, callback) {
  callback([]);
}

function fetchOpenspending(query, location_ids, callback) {
  console.log('Should fetch locations ' + location_ids + ' using openspending now!');
  // FIXME: should fix openspending to allow one call for multiple codes
  // government__code__in
  var url = 'https://openspending.nl/api/v1/documents/?government__code__in=' + location_ids.join(",") + '&order_by=-created_at';
  console.log(url);

  return fetch(
    url, {cache: 'no-cache'}).then(
      response => response.json()
    ).then(
      function (data) {
        var items = [];
        if (typeof(data.objects) !== 'undefined') {
          // FIXME: i.meta.highlight.description is an array!
          items = data.objects.map(function (i) {
            var w = (i.plan == 'budget') ? 'begroting' : 'realisatie';
            var title = w[0].toLocaleUpperCase() + w.slice(1);
            if ((i.period > 0) && (i.period < 5)) {
              title += ' ' + i.period + 'e kwartaal';
            }
            title += ' ' + i.year;
            return {
              key: i.created_at,
              date: i.created_at,
              title: title,
              description: '',
              location: i.government.name,
              type: i.plan == 'budget' ? 'Begroting' : 'Realisatie',
              source: 'openspending',
              url: 'https://openspending.nl/' + i.government.slug + '/' + w + '/' + i.year + '-' + i.period + '/lasten/hoofdfuncties/'
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
            var desc;
            if (typeof(i.meta.highlight) === 'undefined') {
              desc = i.description.substring(0,140);
            } else {
              desc = i.meta.highlight.description;
            }
            return {
              key: i.date,
              date: i.date,
              title: i.title,
              description: desc,
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
