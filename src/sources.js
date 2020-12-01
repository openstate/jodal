export function fetchSource(query, source, location_ids, callback) {
  var source2func = {
    'poliflw': fetchPoliflw,
    'openspending': fetchOpenspending
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

function fetchOpenspending(query, location_ids, callback) {
  console.log('Should fetch locations ' + location_ids + ' using openspending now!');
  // FIXME: should fix openspending to allow one call for multiple codes
  // government__code__in
  var url = 'https://openspending.nl/api/v1/documents/?government__code__in=' + location_ids.join(",") + '&order_by=-created_at';
  console.log(url);

  return fetch(
    url).then(
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
              type: i.plan,
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
      body: JSON.stringify(payload)
    }).then(
      response => response.json()
    ).then(
      function (data) {
        var items = [];
        if (typeof(data.item) !== 'undefined') {
          // FIXME: i.meta.highlight.description is an array!
          items = data.item.map(function (i) {
            return {
              key: i.date,
              date: i.date,
              title: i.title,
              description: i.meta.highlight.description,
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
