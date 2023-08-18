export const binoasDomain = 'api.jodal.nl';

function buildSubscriptionQuery(sources, locations, user_query) {
  var clauses = [];
  var sources_part = [{"match_all": {}}];
  if (sources.langth > 0) {
    sources_part = [
      {
        "term": {
          "data.key": "source"
        }
      },
      {
        "terms": {
          "data.value": sources
        }
      }
    ];
    clauses.push({
      "nested": {
        "path": "data",
        "query": {
          "bool": {
            "must": sources_part
          }
        }
      }
    });
  }
  var locations_part = [{"match_all":{}}];
  // TODO: uhhh
  if (locations.length > 1) {
    locations_part = [
      {
        "term": {
          "data.key": "location"
        }
      },
      {
        "terms": {
          "data.value": locations
        }
      }
    ];
    clauses.push({
        "nested": {
          "path": "data",
          "query": {
            "bool": {
              "must": locations_part
            }
          }
        }
    });
  }
  clauses.push({
      "simple_query_string": {
        "fields": ["title","description"],
        "query": user_query,
        "default_operator": "and"
      }
  });
  return {
    "query": {
      "bool": {
        "must": clauses
      }
    }
  };
}

export function subscriptionNew(user_query, locations, sources, description, email, frequency) {
  var url = window.location.protocol + '//' + binoasDomain + '/subscriptions/new';
  var sub_query = buildSubscriptionQuery(sources, locations, user_query);
  var binoas_def = {
    'application': 'ood',
    'email': email,
    'frequency': frequency,
    'description': description,
    'query': {"query": sub_query.query}
  };
  console.log('sending binoas subscription request:', binoas_def)
  // return fetch(
  //   url, {
  //     method: "POST",
  //     credentials: "include",
  //     body: JSON.stringify(binoas_def),
  //     headers: {
  //       'Content-Type': 'application/json'
  //     }
  //   }).then(
  //     response => response.json()
  //   ).then(
  //     function (data) {
  //       console.log(data);
  //     }
  //   );
  }
