import os
import re
import logging

from flask import Blueprint, session, request, jsonify, send_file

from app.archive import warc_create_archive, warc_archive_status, warc_get_filepath
from app.utils import ensure_authenticated

archive_bp = Blueprint('archive', __name__)

@archive_bp.route('/archive/warc/create')
@ensure_authenticated
def archive_create():
    url = request.args.get('url')
    user = session['user']
    results = warc_create_archive(url, user)
    return jsonify(results)


@archive_bp.route('/archive/warc/<archive_id>')
@ensure_authenticated
def archive_status(archive_id):
    results = warc_archive_status(archive_id)
    return jsonify(results)


@archive_bp.route('/archive/warc/download/<archive_id>')
@ensure_authenticated
def archive_download(archive_id):
    filepath = warc_get_filepath(archive_id)
    logging.info(f'archive {archive_id} => {filepath}')
    return send_file(
        filepath, mimetype='application/warc',
        attachment_filename=os.path.basename(filepath),
        as_attachment=True)


@archive_bp.route('/archive/warcs/<archive_ids_str>')
@ensure_authenticated
def archive_statuses(archive_ids_str):
    archive_ids = re.split(r'\s*,\s*',archive_ids_str)
    results = []
    for a in archive_ids:
        results.append(warc_archive_status(a))
    return jsonify(results)