export const binoasDomain = 'api.jodal.nl';

function buildSubscriptionQuery(sources, locations, user_query) {
  var clauses = [];
  var sources_part = [{"match_all": {}}];
  if (sources.length > 0) {
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
  if (locations.length > 0) {
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
  console.log('sending binoas subscription request:', binoas_def);
  return fetch(
    url, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(binoas_def),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(
      response => response.json()
    );
  }

  export function subscriptionDelete(user_id, query_id) {
    var url = window.location.protocol + '//' + binoasDomain + '/subscriptions/delete';
    var sub_query = buildSubscriptionQuery(sources, locations, user_query);
    var binoas_def = {
      'user_id': user_id,
      'query_id': query_id
    };
    console.log('sending binoas subscription removal request:', binoas_def);
    return fetch(
      url, {
        method: "DELETE",
        credentials: "include",
        body: JSON.stringify(binoas_def),
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(
        response => response.json()
      );
  }
