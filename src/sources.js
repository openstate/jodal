export function fetchSource(query, source, location_ids, callback) {
  var source2func = {
    'poliflw': fetchPoliflw
  }

  var fnc = source2func[source];
  if (typeof(fnc) !== 'undefined') {
    return fnc(query, location_ids, callback);
  }
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
        console.log('got data from periodic fetch! :')
        console.dir(data);
        // FIXME: convert data
        var items = [];
        if (typeof(data.item) !== 'undefined') {
          items = data.item.map(function (i) {
            return {
              key: i.date,
              date: i.date,
              title: i.title,
              description: i.meta.highlight.description,
              location: i.location,
              type: i.source,
              source: 'poliflw'
            };
          });
        }
        callback(items);
      }
    );
}
