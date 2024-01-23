import json
import tempfile
import logging
from io import BytesIO

from flask import Flask, session, render_template, request, redirect, url_for, flash, Markup, jsonify, send_file

import requests
import fitz

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from Flask"

@app.route("/convert")
def convert():
    url = request.args.get('url', '')
    filetype = request.args.get('filetype', 'pdf')
    text = ''
    logging.info('Attempting to retrieve url : %s' % (url,))
    resp = requests.get(url)
    doc=fitz.open(stream=BytesIO(resp.content), filetype=filetype)
    for page in doc: # iterate the document pages
        text += "\n\n" + page.get_text() # get plain text encoded as UTF-8
    logging.info('Converted url : %s' % (url,))
    return json.dumps({
        'url': url,
        'filetype': filetype,
        'text': text
    })

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
