import os
import os.path
import json
import logging
from io import StringIO
import csv

from flask import current_app as app, jsonify, Response

from app.utils import html2text, load_object

from jodal.openspending import OpenSpendingDocumentScraperRunner
from jodal.poliflw import PoliflwDocumentScraperRunner
from jodal.obv import OpenbesluitvormingDocumentScraperRunner

SOURCE2SCRAPER = {
    'openspending': OpenSpendingDocumentScraperRunner,
    'poliflw': PoliflwDocumentScraperRunner,
    'openbesluitvorming': OpenbesluitvormingDocumentScraperRunner
}

SOURCE2PARAM = {
    'openspending': 'document_id',
    'poliflw': 'document_id',
    'openbesluitvorming': 'document_id'
}

FILEFORMAT2MIME = {
    'json': 'application/json',
    'csv': 'text/csv',
    'txt': 'text/plain'
}

FILEFORMAT2CONVERTER = {
    'json': 'convert_for_json',
    'csv': 'convert_for_csv',
    'txt': 'convert_for_txt'
}

SOURCE2CSVFIELDS = {
    'openspending': [
        'locatie','jaar','plan','periode','soort','type','code','naam','bedrag']
}

CACHE_SOURCES = ['openspending']

class Converter(object):
    def convert_for_csv(self, contents, source):
        result = None
        with StringIO() as fp:
            writer = csv.DictWriter(fp, fieldnames=SOURCE2CSVFIELDS[source])
            writer.writeheader()
            for i in contents:
                writer.writerow(i)
            result = fp.getvalue().strip('\r\n')
        return result

    def _clean_contents(sel, contents, source):
        if source == 'poliflw':
            for i in contents:
                i['_source']['title'] = html2text(i['_source'].get('title', ''))
                i['_source']['description'] = html2text(i['_source'].get('description', ''))
        return contents

    def convert_for_json(self, contents, source):
        return json.dumps(self._clean_contents(contents, source))

    def convert_for_txt(self, contents, source):
        output = ""
        for i in self._clean_contents(contents, source):
            output += """
            %s

            %s
            """ % (
                i['_source']['title'], i['_source']['description'],)
        return output

def prepare_download(source, external_item_id, file_format):
    app_name = app.config['NAME_OF_APP']
    setup_es = load_object('%s.es.setup_elasticsearch' % (app_name,))
    es = setup_es(app.config[app_name])

    cache_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '../cache/%s/' % (source,))
    cache_filepath = os.path.join(
        cache_dir, '%s.%s' % (external_item_id, file_format))

    items = None
    logging.info('Checking if %s exists' % (cache_filepath,))
    if os.path.exists(cache_filepath):
        logging.info('%s Exists' % (cache_filepath,))
        with open(cache_filepath) as in_file:
            items = json.load(in_file)

    if items is not None:
        logging.info('Loaded %s items from cache ...' % (len(items,)))
        return items

    try:
        runconfig = {
            'config': app.config,
            SOURCE2PARAM[source]: external_item_id
        }
        items = SOURCE2SCRAPER[source]().run(**runconfig)
    except LookupError as e:
        items = None

    if (items is not None) and (source in CACHE_SOURCES):
        with open(cache_filepath, 'w') as out_file:
            json.dump(items, out_file)

    return items


def perform_download(contents, source, external_item_id, file_format):
    if contents is not None:
        cvt = Converter()
        try:
            file_contents = getattr(cvt, FILEFORMAT2CONVERTER[file_format])(
                contents, source)
        except LookupError as e:
            return jsonify({"status": "error", "msg": "Download mislukt, geen geldige formatter (%s)." % (file_format,)}), 500
        attachment_filepath = '%s.%s' % (external_item_id, file_format)
        return Response(
            file_contents,
            mimetype=FILEFORMAT2MIME[file_format],
            headers={'Content-Disposition':'attachment;filename=%s' % (attachment_filepath,)})
    else:
        return jsonify({"status": "error", "msg": "Download mislukt, geen items."}), 500
