from urllib.parse import urljoin

from flask import Blueprint, request, jsonify, make_response, current_app as app
from feedgen.feed import FeedGenerator

from app.search import perform_query
from app.downloads import prepare_download, perform_download

search_bp = Blueprint('search', __name__)

def make_feed(results, title='Test', description='test', link=None):
    if link is None: link = app.config['JODAL_URL']

    fg = FeedGenerator()
    fg.title(title)
    fg.description(description)
    fg.link(href=link)

    items = results.get('hits', {}).get('hits', [])
    items.reverse()  # ??
    for i in items: # get_news() returns a list of articles from somewhere
        title = i['_source'].get('title') or i['_source'].get('name', '')
        pubDate = i['_source']['published']
        if 'T' not in pubDate:
            pubDate += 'T00:00:00'
        if 'Z' not in pubDate:
            pubDate += 'Z+00:00'
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=urljoin(app.config['JODAL_URL'], 'doc/' + i['_source']['id']))
        desc = i.get('description_clean', '')
        if desc.strip() != '':
            fe.description(desc)
        fe.guid(i['_source']['id'], permalink=False) # Or: fe.guid(article.url, permalink=True)
        fe.pubDate(pubDate)
    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')

    return response

def perform_search(index_name=None, format='json'):
    term = request.args.get('query', '')
    filters = request.args.get('filter', '')
    page = request.args.get('page', '')
    page_size = request.args.get('limit', '10')
    default_operator = request.args.get('default_operator', 'or')
    if format == 'feed':
        default_sort = 'published:desc'
    else:
        default_sort = ''
    sort = request.args.get('sort', default_sort)
    excludes = request.args.get('excludes', 'description')
    includes = request.args.get('includes', '*')
    if not term or term == "null":
        term = "*"

    results = perform_query(
        term, filters, page, int(page_size), sort, includes, excludes,
        default_operator, index_name)
    return results

@search_bp.route("/")
def index():
    term = "*"
    results = perform_query(term, "", 0)
    return jsonify(results)

@search_bp.route('/search')
def search():
    format = request.args.get('format', 'json')
    title = request.args.get('title', 'Test')
    description = request.args.get('description', 'Test')
    results = perform_search(format=format)
    if format == 'feed':
        return make_feed(results, title, description)
    else:
        return jsonify(results)

@search_bp.route('/<index_name>/search')
def search_index(index_name):
    format = request.args.get('format', 'json')
    title = request.args.get('title', 'Test')
    description = request.args.get('description', 'Test')
    results = perform_search('jodal_%s' % (index_name,), format=format)
    if format == 'feed':
        return make_feed(results, title, description)
    else:
        return jsonify(results)

@search_bp.route('/documents/download/<source>/<external_item_id>')
def download(source, external_item_id):
    file_format = request.args.get('format', 'json')
    items = prepare_download(
        source, external_item_id, file_format)
    return perform_download(
        items, source, external_item_id, file_format)
