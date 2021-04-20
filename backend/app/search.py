import logging

from app import app, AppError, load_object



app_name = app.config['NAME_OF_APP']
setup_es = load_object('%s.es.setup_elasticsearch' % (app_name,))
es = setup_es(app.config[app_name])

def perform_query(term, filter_string, page, page_size, sort, index_name=None, doc_type="_doc"):

    filters = parse_filters(filter_string)

    if index_name is None:
        # TODO: query fields adjustable per index, or by query somehow
        query_fields = app.config[app_name]['elasticsearch'].get('query', {}).get('fields', [])
        aggregation_fields = app.config[app_name]['elasticsearch']['aggregations']
    else:
        idx = '_'.join(index_name.split('_')[1:])
        query_fields = app.config[app_name]['elasticsearch'].get('indices', {}).get(idx, {}).get('query', {}).get('fields', [])
        try:
            aggregation_fields = app.config[app_name]['elasticsearch'].get('indices', {}).get(idx, {})['aggregations']
        except KeyError as e:
            aggregation_fields = app.config[app_name]['elasticsearch']['aggregations']

    query = get_basic_query(filters, term, page, page_size, sort, query_fields, aggregation_fields)
    logging.info(query)
    result = es.search(index=index_name, doc_type=doc_type, body=query)

    return result


def parse_filters(filters):
        filter_dict = {}
        for f in filters.split(','):
                if f and len(f.split(':')) == 2:
                        typ = f.split(':')[0]
                        val = f.split(':')[1]
                        filter_dict[typ] = val.split('|')

        return filter_dict


#Those queries implement the filters as AND filter and the query as query_string_query
def get_basic_query(filters, term, page, page_size, sort, query_fields, aggregation_fields):
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
                    clause['range'][real_k]['lt'] = v
                else:
                    clause['range'][real_k]['gte'] = v
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
                "query_string" : { "query" : term, "fields": query_fields }
        }

        query = {
            "query": {
                "bool": {
                    "must": [
                        sqs
                    ]
                }
            },
            "size": page_size,
            "from": start,
            "aggs" : aggregations
        }

        if filters:
            query['query']['bool']['filter'] = filter_clauses

        if len(sort_clause) > 0:
            query['sort'] = sort_clause

        return query
