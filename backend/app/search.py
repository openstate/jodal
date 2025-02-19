import logging

from app.utils import html2text, load_object
from flask import current_app as app
import time

def clean_results(results):
    if len(results.get('hits', {}).get('hits', [])) <= 0:
        return results
    for h in results['hits']['hits']:
        desc = h.get('_source', {}).get('description')
        if desc is not None:
            h['description_clean'] = html2text(desc)
    return results

def perform_query(term, filter_string, page, page_size, sort, includes, excludes, default_operator='or', index_name=None):
    app_name = app.config['NAME_OF_APP']
    setup_es = load_object('%s.es.setup_elasticsearch' % (app_name,))
    es = setup_es(app.config[app_name])

    filters = parse_filters(filter_string)
    logging.info(filters)
    if index_name is None:
        # TODO: query fields adjustable per index, or by query somehow
        query_fields = app.config[app_name]['elasticsearch'].get('query', {}).get('fields', [])
        aggregation_fields = app.config[app_name]['elasticsearch']['aggregations']
        highlighting = app.config[app_name]['elasticsearch'].get('highlight', None)
    else:
        idx = '_'.join(index_name.split('_')[1:])
        query_fields = app.config[app_name]['elasticsearch'].get('indices', {}).get(idx, {}).get('query', {}).get('fields', [])
        try:
            aggregation_fields = app.config[app_name]['elasticsearch'].get('indices', {}).get(idx, {})['aggregations']
        except KeyError as e:
            aggregation_fields = app.config[app_name]['elasticsearch']['aggregations']
        highlighting = app.config[app_name]['elasticsearch'].get('indices', {}).get(idx, {}).get('highlight', None)

    query = get_basic_query(filters, term, page, page_size, sort, includes, excludes, default_operator, query_fields, aggregation_fields, highlighting)
    logging.info(query)
    result = es.search(index=index_name, body=query)

    return clean_results(result)

def perform_aggregation_query(organisation_ids=None):
    app_name = app.config["NAME_OF_APP"]
    setup_es = load_object("%s.es.setup_elasticsearch" % (app_name,))
    es = setup_es(app.config[app_name])

    filters = {}
    if organisation_ids:
        filters = {"location.raw": organisation_ids.split(",")}

    aggregation_fields = {
        "per_source": {
            "terms": {"field": "source", "size": 10},
            "aggs": {
                "total_documents": {"value_count": {"field": "id"}},
                "quarterly_documents": {
                    "date_histogram": {
                        "field": "published",
                        "calendar_interval": "1q",
                        "format": "'Q'Q yyyy",
                        "hard_bounds": {"min": "now-10y"},
                        "extended_bounds": {"min": "now-10y"},
                    }
                },
                "first_date": {"min": {"field": "published", "format": "yyyy-MM-dd"}},
                "last_date": {"max": {"field": "published", "format": "yyyy-MM-dd"}},
            },
        }
    }

    query = get_basic_query(
        filters=filters,
        term="*",
        page=0,
        page_size=1,
        sort=None,
        includes="",
        excludes="",
        default_operator="AND",
        query_fields=["title"],
        aggregation_fields=aggregation_fields,
        highlight=None,
    )

    logging.info(query)

    results = clean_results(es.search(index="jodal_documents", body=query))

    stats = {}
    for bucket in (
        results.get("aggregations", {}).get("per_source", {}).get("buckets", [])
    ):
        source = bucket["key"]
        stats[source] = {
            "total_documents": bucket.get("total_documents", {}).get("value", 0),
            "quarterly_documents": bucket.get("quarterly_documents", {}).get("buckets", []),
            "first_date": bucket.get("first_date", {}).get("value_as_string", None),
            "last_date": bucket.get("last_date", {}).get("value_as_string", None),
        }

    return stats

def parse_filters(filters):
        filter_dict = {}
        for f in filters.split('|'):
                if f and len(f.split(':', 1)) == 2:
                        typ = f.split(':', 1)[0]
                        val = f.split(':', 1)[1]
                        filter_dict[typ] = val.split(',')

        return filter_dict


#Those queries implement the filters as AND filter and the query as query_string_query
def get_basic_query(filters, term, page, page_size, sort, includes, excludes, default_operator, query_fields, aggregation_fields, highlight):
        query = None

        if not page:
                page = 0
        start = int(page) * page_size

        must_clauses = {}
        for k,v in filters.items():
            k_parts = k.split('_')
            real_k = k
            if len(k_parts) == 1:
                clause = {"terms" : { k : v }}
            else:
                real_k = k_parts[0]
                part_k = k_parts[1]
                clause = must_clauses.get(
                    real_k, {
                        'range':{
                            real_k: {}
                        }
                    })
                if part_k == 'to':
                    clause['range'][real_k]['lt'] = v[0]
                else:
                    clause['range'][real_k]['gte'] = v[0]
            must_clauses[real_k] = clause
        filter_clauses = list(must_clauses.values())

        aggregations = aggregation_fields

        sort_clause = []
        if sort:
            for s in sort.split(','):
                fld = s
                order = None
                s_parts = s.split(':')
                if s and len(s_parts) == 2:
                    fld = s_parts[0]
                    order = s_parts[1]
                if order is not None:
                    sort_clause.append({fld:{"order":order}})
                else:
                    sort_clause.append(fld)

        sqs = {
                "query_string" : {
                    "query" : term,
                    "default_operator": default_operator,
                    "fields": query_fields
                }
        }

        query = {
            "query": {
                "bool": {
                    "must": [
                        sqs
                    ]
                }
            },
            "_source": {
              "includes": includes.split(","),
              "excludes": excludes.split(",")
            },
            "size": page_size,
            "from": start,
            "aggs" : aggregations,
            "track_total_hits": True
        }

        if highlight is not None:
                query['highlight'] = highlight
        if filters:
            query['query']['bool']['filter'] = filter_clauses

        if len(sort_clause) > 0:
            query['sort'] = sort_clause

        logging.info(query)

        return query
