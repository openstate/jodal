#!/usr/bin/env python

import hashlib
from glob import glob

import requests
from requests.auth import HTTPDigestAuth
import xmltodict

HERITRIX_URL = 'https://heritrix:8443/engine'
HERITRIX_USER = 'jodal'
HERITRIX_PASSWD = 'jodal'

def heritrix_request(path='', params={}, files=None):
    url = f"{HERITRIX_URL}"
    if path != '':
        url += f"/{path}"
    #print(url)
    resp = requests.post(
        url,
        data=params,
        auth=HTTPDigestAuth(HERITRIX_USER, HERITRIX_PASSWD),
        files=files,
        verify=False)
    if resp.status_code != 200:
        return {"status": "error", "code": resp.status_code}
    return xmltodict.parse(resp.content)

def heritrix_put(path='', params={}, files=None):
    url = f"{HERITRIX_URL}"
    if path != '':
        url += f"/{path}"
    #print(url)
    return requests.put(
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
    ).replace(
        'http://example.example/example', url
    )

def heritrix_job_launch(job_id, checkpoint=None):
    params = {'action': 'launch'}
    if checkpoint is not None:
        params['checkpont'] = checkpoint
    return heritrix_request(f"job/{job_id}", params)

def heritrix_job_pause(job_id):
    return heritrix_request(f"job/{job_id}", {'action': 'pause'})

def heritrix_job_unpause(job_id):
    return heritrix_request(f"job/{job_id}", {'action': 'unpause'})

def heritrix_job_terminate(job_id):
    return heritrix_request(f"job/{job_id}", {'action': 'terminate'})

def heritrix_job_teardown(job_id):
    return heritrix_request(f"job/{job_id}", {'action': 'teardown'})

def heritrix_put_config(job_id, config):
    resp = heritrix_put(f"job/{job_id}/jobdir/crawler-beans.cxml", params=config)
    return resp

def get_warc_archive_id(user_id, url):
    identifier = f"{user_id}\{url}"
    h_id = hashlib.sha1()
    h_id.update(identifier.encode('utf-8'))
    return h_id.hexdigest()

def warc_create_archive(url, user):
    result = {}
    # make identifier base on url + user_id
    hash_id = get_warc_archive_id(user['sub'], url)
    # create new job : https://heritrix.readthedocs.io/en/latest/api.html#create-new-job
    resp = heritrix_job_create(hash_id)
    # get generated config
    content = ''
    with open('./app/files/heritrix.cxml') as in_file:
        content = in_file.read()
    # modify config to add url
    new_config = heritrix_generate_job_config(content, url)
    # TODO: upload new config
    resp4 = heritrix_put_config(hash_id, new_config)
    # build job configuration : https://heritrix.readthedocs.io/en/latest/api.html#build-job-configuration
    resp2 = heritrix_job_build(hash_id)
    # launch job : https://heritrix.readthedocs.io/en/latest/api.html#launch-job
    resp5 = heritrix_job_launch(hash_id)
    resp6 = heritrix_job_unpause(hash_id)

    result['job_id'] = hash_id
    return result


def warc_archive_status(job_id):
    result = {}
        # TODO: get job status : https://heritrix.readthedocs.io/en/latest/api.html#get-job-status
    result = heritrix_request(f"job/{job_id}")

    return result

def warc_get_filepath(job_id):
    try:
        result = sorted(glob(f"/heritrix/jobs/{job_id}/latest/warcs/*.warc.gz"))[-1]
    except LookupError as e:
        result = None
    return result
