export function fetchSource(source, location_ids, callback) {
  var source2func = {
    'poliflw': fetchPoliflw
  }

  var fnc = source2func[source];
  if (typeof(fnc) !== 'undefined') {
    return fnc(location_ids, callback);
  }
}

async function fetchPoliflw(location_ids, callback) {
  console.log('Should fetch locations ' + location_ids + ' using poliflw now!');
  // curl -s 'https://api.poliflw.nl/v0/search' -d '{"filters":{"location":{"terms":["Amsterdam"]}},"size":0}'
  var url = 'https://api.poliflw.nl/v0/search';
  var payload = {
    "filters":{
      "location":{
        "terms": location_ids
      }
    },
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
        callback(data);
      }
    );
}
