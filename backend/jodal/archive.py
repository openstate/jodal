#!/usr/bin/env python

import hashlib

def get_warc_archive_id(user_id, url):
    identifier = f"{user_id}\{url}"
    h_id = hashlib.sha1()
    h_id.update(identifier.encode('utf-8'))
    return h_id.hexdigest()

def warc_create_archive(url, user):
    result = {}
    # make identifier base on url + user_id
    hash_id = get_warc_archive_id(user['id'], url)
    # TODO: create new job : https://heritrix.readthedocs.io/en/latest/api.html#create-new-job
    # TODO: build job configuration : https://heritrix.readthedocs.io/en/latest/api.html#build-job-configuration
    # TODO: launch job : https://heritrix.readthedocs.io/en/latest/api.html#launch-job
    return result


def warc_archive_status(archive_id):
    result = {}
        # TODO: get job status : https://heritrix.readthedocs.io/en/latest/api.html#get-job-status
    return result
