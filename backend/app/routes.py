import json
from functools import wraps
import logging
import traceback

from flask import render_template, request, redirect, url_for, flash, Markup, jsonify

from app import app, AppError
from app.search import perform_query


def decode_json_post_data(fn):
    """Decorator that parses POSTed JSON and attaches it to the request
    object (:obj:`request.data`)."""

    @wraps(fn)
    def wrapped_function(*args, **kwargs):
        if request.method in ['POST', 'DELETE']:
            data = request.get_data(cache=False)
            if not data:
                raise AppError('No data was POSTed', 400)

            try:
                request_charset = request.mimetype_params.get('charset')
                if request_charset is not None:
                    data = json.loads(data, encoding=request_charset)
                else:
                    data = json.loads(data)
            except:
                raise AppError('Unable to parse POSTed JSON', 400)

            request.data = data

        return fn(*args, **kwargs)

    return wrapped_function



@app.route("/")
def index():
    term = "*"
    results = perform_query(term, "", 0)
    return jsonify(results)


@app.route('/search')
def search():
    term = request.args.get('term', '')
    filters = request.args.get('filter', '')
    page = request.args.get('page', '')
    page_size = request.args.get('limit', '10')
    sort = request.args.get('sort', '')
    if not term or term == "null":
        term = "*"

    results = perform_query(term, filters, page, int(page_size), sort)

    return jsonify(results)


if __name__ == "__main__":
    app.run(threaded=True)
