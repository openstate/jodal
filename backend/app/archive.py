#!/usr/bin/env python

import hashlib

import requests
from requests.auth import HTTPDigestAuth

HERITRIX_URL = 'https://heritrix:8443/engine'
HERITRIX_USER = 'jodal'
HERITRIX_PASSWD = 'jodal'

def heritrix_request(path='', params={}):
    url = f"{HERITRIX_URL}"
    if path != '':
        url += f"/{path}"
    return requests.post(
        url,
        data=params,
        auth=HTTPDigestAuth(HERITRIX_USER, HERITRIX_PASSWD),
        verify=False)

def heritrix_job_create(job_id):
    resp = heritrix_request({'action': 'create', 'createpath': job_id})
    return resp

def heritrix_job_status(job_id):
    resp = heritrix_request(f"job/{job_id}")
    return resp

def get_warc_archive_id(user_id, url):
    identifier = f"{user_id}\{url}"
    h_id = hashlib.sha1()
    h_id.update(identifier.encode('utf-8'))
    return h_id.hexdigest()

def warc_create_archive(url, user):
    result = {}
    # make identifier base on url + user_id
    hash_id = get_warc_archive_id(user['id'], url)
    # create new job : https://heritrix.readthedocs.io/en/latest/api.html#create-new-job
    resp = heritrix_job_create(hash_id)
    # TODO: build job configuration : https://heritrix.readthedocs.io/en/latest/api.html#build-job-configuration
    # TODO: launch job : https://heritrix.readthedocs.io/en/latest/api.html#launch-job
    return result


def warc_archive_status(archive_id):
    result = {}
        # TODO: get job status : https://heritrix.readthedocs.io/en/latest/api.html#get-job-status
    return result
