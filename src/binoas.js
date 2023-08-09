export const binoasDomain = 'binoas.openstate.eu';

function buildSubscriptionQuery(sources, locations, user_query) {
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
  }
  var locations_part = [{"match_all":{}}];
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
  }
  return {
    "query": {
      "bool": {
        "must": [
          {
            "nested": {
              "path": "data",
              "query": {
                "bool": {
                  "must": sources_part
                }
              }
            }
          },


          {
            "nested": {
              "path": "data",
              "query": {
                "bool": {
                  "must": locations_part
                }
              }
            }
          },

          {
            "simple_query_string": {
              "fields": ["title","description"],
              "query": user_query,
              "default_operator": "and"
            }
          }
        ]
      }
    }
  };
}

export function subscriptionNew(user_query, locations, sources, description, email, frequency) {
  var url = window.location.protocol + '//' + binoasDomain + '/subscriptions/new';
  var binoas_def = {
    'application': 'ood',
    'email': email,
    'frequency': frequency,
    'description': description,
    'query': {}
  };
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
    ).then(
      function (data) {
        console.log(data);
      }
    );
  }

}
