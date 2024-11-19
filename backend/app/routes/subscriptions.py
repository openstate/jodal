
import logging
import hashlib

from flask import Blueprint, current_app as app, request, jsonify
import requests

from app.fa import setup_fa
from app.utils import decode_json_post_data

subscriptions_bp = Blueprint('subscriptions', __name__)

@subscriptions_bp.route("/subscriptions/new", methods=["POST"])
@decode_json_post_data
def subscriptions_new():
    email = request.data.get('email', None)
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
            # res = _passwordless_start(client, email)
            # if (res is not None) and ('error' in res):
            #     return jsonify(res)
            return jsonify(resp.json())
    return jsonify(resp.json())

@subscriptions_bp.route("/subscriptions/delete", methods=["GET"])
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