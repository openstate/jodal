import os
import json
from functools import wraps
import logging
import traceback

from flask import Flask, session, render_template, request, redirect, url_for, flash, Markup, jsonify, send_file
from requests_oauthlib import OAuth2Session
from fusionauth.fusionauth_client import FusionAuthClient
import pkce
import requests

from app import app, db, AppError
from app.search import perform_query
from app.models import Column, UserData
from app.downloads import prepare_download, perform_download
from app.user import delete_user_data

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


def perform_search(index_name=None):
    term = request.args.get('query', '')
    filters = request.args.get('filter', '')
    page = request.args.get('page', '')
    page_size = request.args.get('limit', '10')
    sort = request.args.get('sort', '')
    if not term or term == "null":
        term = "*"

    results = perform_query(
        term, filters, page, int(page_size), sort, index_name)
    return results


@app.route("/")
def index():
    term = "*"
    results = perform_query(term, "", 0)
    return jsonify(results)


@app.route("/users/simple/me")
def do_me():
    if session.get('user') != None:
        user = session['user']
    else:
        user = None
    return jsonify(user)


@app.route("/users/simple/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(app.config['FA_URL']+'/oauth2/logout?client_id='+app.config['CLIENT_ID'])



@app.route("/users/simple/login", methods=["GET"])
def login():
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    fusionauth = OAuth2Session(app.config['CLIENT_ID'], redirect_uri=app.config['REDIRECT_URI'])
    authorization_url, state = fusionauth.authorization_url(app.config['AUTHORIZATION_BASE_URL'])
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    # save the verifier in session to send it later to the token endpoint
    session['code_verifier'] = code_verifier
    return redirect(authorization_url+'&code_challenge='+code_challenge+'&code_challenge_method=S256')


@app.route("/users/simple/register", methods=["GET"])
def register():
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    fusionauth = OAuth2Session(app.config['CLIENT_ID'], redirect_uri=app.config['REDIRECT_URI'])
    authorization_url, state = fusionauth.authorization_url(app.config['AUTHORIZATION_BASE_URL'])

    # registration lives under non standard url, but otherwise takes exactly the same parameters
    registration_url = authorization_url.replace("authorize", "register", 1)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    # save the verifier in session to send it later to the token endpoint
    session['code_verifier'] = code_verifier
    return redirect(registration_url+'&code_challenge='+code_challenge+'&code_challenge_method=S256')


@app.route("/users/simple/callback", methods=["GET"])
def callback():
    expected_state = session['oauth_state']
    state = request.args.get('state','')
    auth_code = request.args.get('code','')
    if state != expected_state:
        return jsonify({"error": "Error, state doesn't match, redirecting without getting token."}), 500

    # call token endpoint url
    resp = requests.post(
        url=app.config['TOKEN_URL'],
        data={
            'grant_type': 'authorization_code',
            'client_id': app.config['CLIENT_ID'],
            'client_secret': app.config['CLIENT_SECRET'],
            'redirect_uri': app.config['REDIRECT_URI'],
            'code': auth_code,
            'code_verifier': session['code_verifier']
        }
    )
    result = resp.json()
    token_dict = {
        'access_token': result['access_token'],
        'token_type': 'bearer'
    }

    fusionauth = OAuth2Session(client_id=app.config['CLIENT_ID'], token=token_dict)
    session['oauth_token'] = result['access_token']
    session['user'] = fusionauth.get(app.config['USERINFO_URL']).json()

    test_cookie = request.cookies.get('jodal_abtest')
    if test_cookie is not None:
        user_id = session['user']['sub']
        ud = UserData(
            user_id=user_id,
            key='abtest',
            value=test_cookie
        )
        db.session.add(ud)
        utm_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content' ,'utm_term']
        for utm_param in utm_params:
            utm_val = request.cookies.get('jodal_' + utm_param)
            if utm_val is not None:
                ud2 = UserData(
                    user_id=user_id,
                    key=utm_param,
                    value=utm_val
                )
                db.session.add(ud2)
        db.session.add(ud)
        db.session.commit()

    # return redirect('/users/simple/me')
    return redirect(app.config['JODAL_URL'])


@app.route("/users/delete")
def do_delete():
    if session.get('user') != None:
        user = session['user']
    else:
        user = None
    if user is None:
        return redirect(app.config['JODAL_URL'])

    # first delete associated user data
    delete_user_data(user['sub'])

    # Delete User For A Given ID
    client = FusionAuthClient(app.config['API_KEY'], app.config['FA_INTERNAL_URL'])
    client_response =client.delete_user(user['sub'])
    if client_response.was_successful():
        session.clear()
        return redirect(app.config['FA_URL']+'/oauth2/logout?client_id='+app.config['CLIENT_ID'])
    else:
        return redirect(app.config['JODAL_URL'])


@app.route('/documents/download/<source>/<external_item_id>')
def download(source, external_item_id):
    file_format = request.args.get('format', 'json')
    items = prepare_download(
        source, external_item_id, file_format)
    return perform_download(
        items, source, external_item_id, file_format)


@app.route('/search')
def search():
    results = perform_search()
    return jsonify(results)


@app.route('/<index_name>/search')
def search_index(index_name):
    results = perform_search('jodal_%s' % (index_name,))
    return jsonify(results)

if __name__ == "__main__":
    app.run(threaded=True)
