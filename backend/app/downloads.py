import os
import json
from functools import wraps
import logging
from io import StringIO, BytesIO

from flask import Flask, session, render_template, request, redirect, url_for, flash, Markup, jsonify, send_file, Response

from app import app, AppError, load_object
from app.search import perform_query
from app.models import Column

from jodal.openspending import OpenSpendingDocumentScraperRunner

SOURCE2SCRAPER = {
    'openspending': OpenSpendingDocumentScraperRunner
}

SOURCE2PARAM = {
    'openspending': 'document_id'
}

FILEFORMAT2MIME = {
    'json': 'application/json'
}

def prepare_download(source, external_item_id, file_format):
    app_name = app.config['NAME_OF_APP']
    setup_es = load_object('%s.es.setup_elasticsearch' % (app_name,))
    es = setup_es(app.config[app_name])

    runconfig = {
        'config': app.config,
        SOURCE2PARAM[source]: external_item_id
    }

    items = SOURCE2SCRAPER[source]().run(**runconfig)

    return items

def perform_download(contents, external_item_id, file_format):
    json_contents = json.dumps(contents)
    attachment_filepath = '%s.%s' % (external_item_id, file_format)
    # return send_file(
    #     fp, mimetype=FILEFORMAT2MIME[file_format], as_attachment=True,
    #     attachment_filename=attachment_filepath)
    return Response(json_contents,
        mimetype=FILEFORMAT2MIME[file_format],
        headers={'Content-Disposition':'attachment;filename=%s' % (attachment_filepath,)})
