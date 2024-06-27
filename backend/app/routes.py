import os
import re
import json
from functools import wraps
import logging
import traceback
import hashlib
from urllib.parse import urljoin

from flask import Flask, session, render_template, request, redirect, url_for, flash, Markup, jsonify, send_file, make_response
from requests_oauthlib import OAuth2Session
from fusionauth.fusionauth_client import FusionAuthClient
import pkce
import requests
from feedgen.feed import FeedGenerator

from app import app, db, AppError
from app.fa import setup_fa
from app.search import perform_query
from app.models import Column, UserData, Asset
from app.downloads import prepare_download, perform_download
from app.user import delete_user_data
from app.archive import warc_create_archive, warc_archive_status, warc_get_filepath

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

def ensure_authenticated(fn):
    """"Decorator thst cheks if user is logged in"""
    @wraps(fn)
    def wrapped_function(*args, **kwargs):
        if session.get('user') != None:
            user = session['user']
        else:
            user = None
        if user is None:
            raise AppError('Not logged in', 403)
        return fn(*args, **kwargs)

    return wrapped_function


def make_feed(results, title='Test', description='test', link=app.config['JODAL_URL']):
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
        term, filters, page, int(page_size), sort, includes, excludes, index_name)
    return results


def convert_userinfo(user):
    result = {
        'applicationId': app.config['CLIENT_ID'],
        'email': user['email'],
        'email_verified': user['verified'],
        'family_name': user.get('lastName'),
        'given_name': user.get('firstName'),
        'roles': [],
        'sub': user['id']
    }
    return result

@app.route("/")
def index():
    term = "*"
    results = perform_query(term, "", 0)
    return jsonify(results)


@app.route("/subscriptions/new", methods=["POST"])
@decode_json_post_data
def subscriptions_new():
    email = request.data.get('email', None)
    # Delete User For A Given ID
    client = setup_fa()

    if email is None:
        return jsonify({'error': 'Empty email'})

    logging.info(request.data)
    resp = requests.post(
        url='http://binoas.openstate.eu/subscriptions/new',
        json=dict(request.data)
    )

    client_resp = client.retrieve_user_by_email(email)
    if not client_resp.was_successful():
        client_response = client.register({
            'sendSetPasswordEmail': False,
            'registration': {
                'applicationId': app.config['CLIENT_ID'],
            },
            'user': {
                'email': email,
                'password': hashlib.md5(email.encode('ascii', 'replace')).hexdigest()
            }
        })
        # result = resp.json()

        if not client_response.was_successful():
            return jsonify(client_response.error_response)
        else:
            # TODO: add sending passwordless login here
            res = _passwordless_start(client, email)
            if (res is not None) and ('error' in res):
                return jsonify(res)
    return jsonify(resp.json())

@app.route("/subscriptions/delete", methods=["GET"])
def subscriptions_delete():
    resp = requests.delete(
        url='http://binoas.openstate.eu/subscriptions/delete',
        json={
            'query_id': request.args.get('query_id', ''),
            'user_id': request.args.get('user_id', '')
        }
    )
    try:
        result = resp.json()
    except Exception as e:
        result = {'error': 'Er ging iets verkeerd', 'status': 'error', 'msg': str(resp.content)}
    return jsonify(result)

def _passwordless_start(client, email):
    client_response = client.start_passwordless_login({
        'applicationId': app.config['CLIENT_ID'],
        'loginId': email
    })

    if not client_response.was_successful():
        return {"error": "Some kind of error: %s" % (client_response.error_response,)}

    logging.info('Started password login succesfully for %s' % (email,))

    send_response = client.send_passwordless_code(
        client_response.success_response)

    if send_response.was_successful():
        logging.info('Sent password login succesfully for %s' % (email,))
        return send_response.success_response
    else:
        return {"error": "Some kind of error: %s" % (send_response.error_response,)}

@app.route("/users/passwordless/start", methods=["GET"])
def api_passwordless_start():
    client = setup_fa()

    email = request.args.get('email','')
    user_id = request.args.get('user_id', '')

    if user_id.strip() != '':
        resp = requests.get('http://binoas.openstate.eu/users?id=%s' % (user_id,))
        if resp.status_code == 200:
            j = resp.json()

            results = j.get('results', [])
            try:
                email = results[0]['email']
            except LookupError as e:
                email = ''

    if email.strip() == '':
        return jsonify({"error": "Email was empty or not found"})

    return jsonify(_passwordless_start(client, email))

@app.route("/users/passwordless/complete", methods=["GET"])
def api_passwordless_complete():
    client = setup_fa()

    code = request.args.get('code','')

    if code.strip() == '':
        return jsonify({"error": "Code was empty"})

    client_response = client.passwordless_login({
        'applicationId': app.config['CLIENT_ID'],
        'code': code
    })
    # result = resp.json()

    if not client_response.was_successful():
        #return jsonify({"error": "Some kind of error: %s" % (client_response.error_response,)})
        return redirect(urljoin(app.config['JODAL_URL'], '/login'))

    session['oauth_token'] = client_response.success_response['token']
    session['user'] = convert_userinfo(client_response.success_response['user'])

    #return jsonify(client_response.success_response)
    return redirect(app.config['JODAL_URL'])

@app.route("/users/login", methods=["POST", "GET"])
def api_login():

    # Delete User For A Given ID
    client = setup_fa()

    loginId = request.args.get('email') or request.form['email']
    passwd = request.args.get('password') or request.form['password']
    client_response = client.login({
        'applicationId': app.config['CLIENT_ID'],
        'loginId': loginId,
        'password': passwd
    })
    # result = resp.json()

    if client_response.was_successful():
        # return redirect('/users/simple/me')
        session['oauth_token'] = client_response.success_response['token']
        session['user'] = convert_userinfo(client_response.success_response['user'])

        return redirect(app.config['JODAL_URL'])
        # return jsonify(session['user'])
    else:
        return jsonify({"error": "Some kind of error: %s" % (client_response.error_response,)})

@app.route("/users/forgot-password", methods=["POST"])
def api_forgot():

    # Delete User For A Given ID
    client = setup_fa()

    client_response = client.forgot_password({
        'applicationId': app.config['CLIENT_ID'],
        'loginId': request.form['email']
    })
    # result = resp.json()

    if client_response.was_successful():
        return redirect(app.config['JODAL_URL'])
        # return jsonify(session['user'])
    else:
        return jsonify({"error": "Some kind of error: %s" % (client_response.error_response,)})


@app.route("/users/register", methods=["POST"])
def api_register():

    # Delete User For A Given ID
    client = setup_fa()

    client_response = client.register({
        'registration': {
            'applicationId': app.config['CLIENT_ID'],
        },
        'user': {
            'email': request.form['email'],
            'password': request.form['password']
        }
    })
    # result = resp.json()

    if client_response.was_successful():
        # return redirect('/users/simple/me')
        session['oauth_token'] = client_response.success_response['token']
        session['user'] = convert_userinfo(client_response.success_response['user'])

        return redirect(app.config['JODAL_URL'])
        # return jsonify(session['user'])
    else:
        return jsonify({"error": "Some kind of error: %s" % (client_response.error_response,)})


@app.route("/users/simple/me")
def do_me():
    # Delete User For A Given ID
    client = setup_fa()

    logging.info('session:')
    logging.info(dict(session))
    if 'oauth_token' not in session:
        user = None
    else:
        client_response = client.validate_jwt(session['oauth_token'])
        if client_response.was_successful():
            if session.get('user') != None:
                user = session['user']
            else:
                user = None
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


@app.route("/user/simple/register/", methods=["GET"])
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
    client = setup_fa()
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


@app.route('/archive/warc/create')
@ensure_authenticated
def archive_create():
    url = request.args.get('url')
    user = session['user']
    results = warc_create_archive(url, user)
    return jsonify(results)


@app.route('/archive/warc/<archive_id>')
@ensure_authenticated
def archive_status(archive_id):
    results = warc_archive_status(archive_id)
    return jsonify(results)


@app.route('/archive/warc/download/<archive_id>')
@ensure_authenticated
def archive_download(archive_id):
    filepath = warc_get_filepath(archive_id)
    logging.info(f'archive {archive_id} => {filepath}')
    return send_file(
        filepath, mimetype='application/warc',
        attachment_filename=os.path.basename(filepath),
        as_attachment=True)


@app.route('/archive/warcs/<archive_ids_str>')
@ensure_authenticated
def archive_statuses(archive_ids_str):
    archive_ids = re.split(r'\s*,\s*',archive_ids_str)
    results = []
    for a in archive_ids:
        results.append(warc_archive_status(a))
    return jsonify(results)

@app.route('/search')
def search():
    format = request.args.get('format', 'json')
    title = request.args.get('title', 'Test')
    description = request.args.get('description', 'Test')
    results = perform_search(format=format)
    if format == 'feed':
        return make_feed(results, title, description)
    else:
        return jsonify(results)


@app.route('/<index_name>/search')
def search_index(index_name):
    format = request.args.get('format', 'json')
    title = request.args.get('title', 'Test')
    description = request.args.get('description', 'Test')
    results = perform_search('jodal_%s' % (index_name,), format=format)
    if format == 'feed':
        return make_feed(results, title, description)
    else:
        return jsonify(results)

if __name__ == "__main__":
    app.run(threaded=True)
