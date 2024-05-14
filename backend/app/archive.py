#!/usr/bin/env python

import hashlib

import requests
from requests.auth import HTTPDigestAuth

HERITRIX_URL = 'https://heritrix:8443/engine'
HERITRIX_USER = 'jodal'
HERITRIX_PASSWD = 'jodal'

def heritrix_request(path='', params={}, files=None):
    url = f"{HERITRIX_URL}"
    if path != '':
        url += f"/{path}"
    print(url)
    return requests.post(
        url,
        data=params,
        auth=HTTPDigestAuth(HERITRIX_USER, HERITRIX_PASSWD),
        files=files,
        verify=False)

def heritrix_job_create(job_id):
    resp = heritrix_request(params={'action': 'create', 'createpath': job_id})
    return resp

def heritrix_job_build(job_id):
    resp = heritrix_request(f"job/{job_id}", {'action': 'build'})
    return resp

def heritrix_job_status(job_id):
    resp = heritrix_request(f"job/{job_id}")
    return resp

def heritrix_job_get_config(job_id):
    resp = heritrix_request(f"job/{job_id}/jobdir/crawler-beans.cxml")
    return resp

def heritrix_generate_job_config(orig_template, url):
    return orig_template.replace(
        '# [see override above]', url
    ).replace(
        'ENTER_AN_URL_WITH_YOUR_CONTACT_INFO_HERE_FOR_WEBMASTERS_AFFECTED_BY_YOUR_CRAWL', 'https://bron.live/'
    )

def get_warc_archive_id(user_id, url):
    identifier = f"{user_id}\{url}"
    h_id = hashlib.sha1()
    h_id.update(identifier.encode('utf-8'))
    return h_id.hexdigest()

def warc_create_archive(url, user):
    result = {}
    # make identifier base on url + user_id
    hash_id = get_warc_archive_id(user['id'], url)
    print(f"Hash: {hash_id}")
    # create new job : https://heritrix.readthedocs.io/en/latest/api.html#create-new-job
    resp = heritrix_job_create(hash_id)
    # build job configuration : https://heritrix.readthedocs.io/en/latest/api.html#build-job-configuration
    #resp2 = heritrix_job_build(hash_id)
    # get generated config
    content = ''
    with open('./app/files/heritrix.cxml') as in_file:
        content = in_file.read()
    # modify config to add url
    new_config = heritrix_generate_job_config(content, url)
    print(new_config)
    # TODO: upload new config
    # TODO: launch job : https://heritrix.readthedocs.io/en/latest/api.html#launch-job
    return result


def warc_archive_status(archive_id):
    result = {}
        # TODO: get job status : https://heritrix.readthedocs.io/en/latest/api.html#get-job-status
    return result
