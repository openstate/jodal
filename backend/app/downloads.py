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

FILEFORMAT2CONVERTER = {
    'json': 'convert_for_json'
}

class Converter(object):
    def convert_for_json(self, contents):
        return json.dumps(contents)

def prepare_download(source, external_item_id, file_format):
    app_name = app.config['NAME_OF_APP']
    setup_es = load_object('%s.es.setup_elasticsearch' % (app_name,))
    es = setup_es(app.config[app_name])

    try:
        runconfig = {
            'config': app.config,
            SOURCE2PARAM[source]: external_item_id
        }
        items = SOURCE2SCRAPER[source]().run(**runconfig)
    except LookupError as e:
        items = None

    return items


def perform_download(contents, external_item_id, file_format):
    if contents is not None:
        cvt = Converter()
        try:
            file_contents = getattr(cvt, FILEFORMAT2CONVERTER[file_format])(contents)
        except LookupError as e:
            return jsonify({"status": "error", "msg": "Download mislukt."}), 500
        attachment_filepath = '%s.%s' % (external_item_id, file_format)
        return Response(
            file_contents,
            mimetype=FILEFORMAT2MIME[file_format],
            headers={'Content-Disposition':'attachment;filename=%s' % (attachment_filepath,)})
    else:
        return jsonify({"status": "error", "msg": "Download mislukt."}), 500
