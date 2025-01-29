import logging
from urllib.parse import urljoin

from flask import Blueprint, current_app as app, session, request, redirect, jsonify
from requests_oauthlib import OAuth2Session
import pkce
import requests

from app.fa import setup_fa
from app.models import UserData
from app.user import delete_user_data
from app.extensions import db

users_bp = Blueprint('users', __name__)

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

@users_bp.route("/users/login", methods=["POST", "GET"])
def api_login():
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

        #return redirect(app.config['JODAL_URL'])
        return jsonify(session['user']), 200
    else:
        return jsonify({
            "error": "Some kind of error: %s" % (client_response.error_response,),
            "content": str(client_response.response.content),
        }), 400

@users_bp.route("/users/forgot-password", methods=["POST"])
def api_forgot_password():
    client = setup_fa()

    client_response = client.forgot_password({
        'applicationId': app.config['CLIENT_ID'],
        'loginId': request.form['email']
    })
    # result = resp.json()

    if client_response.was_successful():
        return jsonify({"success": "true"})
        # return jsonify(session['user'])
    else:
        return jsonify({"error": "Some kind of error: %s" % (client_response.error_response,)}), 400

@users_bp.route("/users/change-password", methods=["POST"])
def api_change_password():
    client = setup_fa()

    password1 = request.form['password']
    password2 = request.form['password_repeat']

    if password1 != password2:
        return jsonify({"error": "Passwords don't match"})

    client_response = client.change_password(request.form["changePasswordId"], {
        "changePasswordId": request.form["changePasswordId"],
        "password": password1
    })
    # result = resp.json()

    if client_response.was_successful():
        # return redirect(app.config['JODAL_URL'])
        return jsonify({ "success": "true" })
    else:
        return jsonify({"error": "Some kind of error: %s" % (client_response.error_response,)}), 400

@users_bp.route("/users/register", methods=["POST"])
def api_register():
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

        # return redirect(app.config['JODAL_URL'])
        return jsonify(session['user'])
    else:
        return jsonify({
            "error": "Some kind of error: %s" % (client_response.error_response,),
            "content":str(client_response.response.content),
        }), 400

@users_bp.route("/users/logout", methods=["POST"])
def api_logout():
    client = setup_fa()
    clients_response = client.logout("false")
    if clients_response.was_successful():
        session.clear()
        return jsonify({ "success": "true" })
    else:
        return jsonify({"error": "Some kind of error: %s" % (clients_response.error_response,)}), 400

@users_bp.route("/users/verify", methods=["GET"])
def api_verify():
    client = setup_fa()
    clients_response = client.verify_email(request.args.get('id'))
    success = clients_response.was_successful()
    return jsonify({ "success": success }), 200 if success else 400

@users_bp.route("/users/simple/me")
def do_me():
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

@users_bp.route("/users/passwordless/start", methods=["GET"])
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

@users_bp.route("/users/passwordless/complete", methods=["GET"])
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

@users_bp.route("/users/simple/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(app.config['FA_URL']+'/oauth2/logout?client_id='+app.config['CLIENT_ID'])



@users_bp.route("/users/simple/login", methods=["GET"])
def login():
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    fusionauth = OAuth2Session(app.config['CLIENT_ID'], redirect_uri=app.config['REDIRECT_URI'])
    authorization_url, state = fusionauth.authorization_url(app.config['AUTHORIZATION_BASE_URL'])
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    # save the verifier in session to send it later to the token endpoint
    session['code_verifier'] = code_verifier
    return redirect(authorization_url+'&code_challenge='+code_challenge+'&code_challenge_method=S256')


@users_bp.route("/user/simple/register/", methods=["GET"])
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


@users_bp.route("/users/simple/callback", methods=["GET"])
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


@users_bp.route("/users/delete")
def do_delete():
    if session.get('user') != None:
        user = session['user']
    else:
        user = None
    if user is None:
        return redirect(app.config['JODAL_URL'])

    # first delete associated user data
    delete_user_data(user['sub'])

    client = setup_fa()
    client_response =client.delete_user(user['sub'])
    if client_response.was_successful():
        session.clear()
        return redirect(app.config['FA_URL']+'/oauth2/logout?client_id='+app.config['CLIENT_ID'])
    else:
        return redirect(app.config['JODAL_URL'])