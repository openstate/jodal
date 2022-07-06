#!/usr/bin/env python3

import sys
import os
import os.path
import argparse
from glob import glob
from os.path import basename, splitext
import json
from pathlib import Path
from pprint import pprint
from itertools import islice, chain
from time import sleep
import datetime

# Import alephclient:
from alephclient.api import AlephAPI

# Load the followthemoney data model:
from followthemoney import model

def load_meta(f):
    result = None
    with open(f, 'r') as in_file:
        result = json.load(in_file)
    return result

def create_link(document_id, muni_id, start_date=None, end_date=None):
    # Create the link entity proxy:
    link_proxy = model.make_entity('UnknownLink')

    # We'll derive the link ID from the other two IDs here, but
    # this could be any unique value (make sure it does not clash
    # with the ID for the main entity!)
    link_proxy.make_id('link', muni_id, document_id)

    # Now we assign the two ends of the link. Note that we can just
    # pass in a proxy object:
    link_proxy.add('subject', muni_id)
    link_proxy.add('object', document_id)
    link_proxy.add('role', 'Period')
    if start_date is not None:
        link_proxy.add('startDate', start_date)
    if end_date is not None:
        link_proxy.add('endDate', end_date)
    return link_proxy

def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))

def main(argv):
    parser = argparse.ArgumentParser(description='Load data into Aleph')
    parser.add_argument('-f', '--foreign-id', default='decentrale_regelgeving', help='foreign id for Aleph')
    parser.add_argument('-d', '--data-path', default='decentrale_regelgeving', help='Path to the data files')
    parser.add_argument('-b', '--batch-size', default=1, type=int, help='Batch size for uploading to Aleph')
    parser.add_argument('-s', '--sleep', default=0, type=int, help='Sleep time between batches')
    parser.add_argument('-m', '--modified', default=datetime.datetime.now() - datetime.timedelta(days=1),
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),)
    parsed_args = parser.parse_args(argv[1:])

    # By default, alephclient will read host and API key from the
    # environment. You can also pass both as an argument here:
    api = AlephAPI()

    # Get the collection (dataset)
    data_path = parsed_args.data_path
    foreign_id = parsed_args.foreign_id

    collection = api.load_collection_by_foreign_id(foreign_id)
    collection_id = collection.get('id')

    gemeenten = {}

    for i in api.stream_entities(collection, schema='PublicBody'):
        for n in i['properties']['name']:
            gemeenten[n] = i

    document_links = []
    for f in glob('%s/*.json' % (data_path,)):
        print(f)
        root, ext = splitext(f)
        meta = load_meta(f)
        if 'id' not in meta.keys():
            print("No id for crawled result, continuing")
            continue
        if 'modified_at' in meta.keys():
            mod_date = datetime.datetime.strptime(
                meta['modified_at'].split('T')[0], '%Y-%m-%d')
            if mod_date < parsed_args.modified:
                print("Modification date was not in range")
                continue
        html_file = '%s/%s' % (data_path,meta['_file_name'],)
        if not os.path.exists(html_file):
            print("No html file (%s) for crawled result, continuing," % (html_file,))
            continue
        metadata = {
            'file_name': '%s.html' % (meta['id'],)
        }
        meta.update(metadata)
        result = api.ingest_upload(collection_id, Path(html_file), meta)
        document_id = result.get('id')
        cleaned_name = meta['author'].replace('Gemeente ', '')
        if cleaned_name in gemeenten:
            municipality_id = gemeenten[cleaned_name].get('id')
            if municipality_id is not None:
                document_links.append(
                    create_link(
                        document_id, municipality_id,
                        meta.get('start_date'), meta.get('end_date')))
        # file_path = 'www.personadeinteres.org/uploads/example.pdf'
        # metadata = {'file_name': 'example.pdf'}
        # # Upload the document:
        # result = api.ingest_upload(collection_id, file_path, metadata)
        #
        # # Finally, we have an entity ID:
        # document_id = result.get('id')
        batch_count = 0
        if len(document_links) >= parsed_args.batch_size:
            entities = [l.to_dict() for l in document_links]
            # You can also feed an iterator to write_entities if you
            # want to upload a very large
            api.write_entities(collection_id, entities)
            batch_count += 1
            print("Uploaded %s batches to Aleph" % (batch_count,))
            document_links = []
            sleep(parsed_args.sleep)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
