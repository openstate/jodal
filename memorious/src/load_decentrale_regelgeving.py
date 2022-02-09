from glob import glob
from os.path import basename, splitext
import json
from pathlib import Path

# Import alephclient:
from alephclient.api import AlephAPI

# Load the followthemoney data model:
from followthemoney import model

def load_meta(f):
    result = None
    with open(f, 'r') as in_file:
        result = json.load(in_file)
    return result

def create_link(doc_id, muni_id, start_date=None, end_date=None):
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

# By default, alephclient will read host and API key from the
# environment. You can also pass both as an argument here:
api = AlephAPI()

# Get the collection (dataset)
foreign_id = 'decentrale_regelgeving'
data_path = '/data/results/%s' % (foreign_id)
collection = api.load_collection_by_foreign_id(foreign_id)
collection_id = collection.get('id')

gemeenten = {}

for i in api.stream_entities(collection, schema='PublicBody'):
    print(i)
    for n in i['properties']['name']:
        gemeenten[n] = i

document_links = []
for f in glob('%s/*.json' % (data_path,)):
    # print(f)
    root, ext = splitext(f)
    print(root, ext)
    meta = load_meta(f)
    print(meta)
    if 'id' not in meta.keys():
        print("No id for crawled result, continuing")
        continue
    html_file = '%s.data.html' % (root,)
    metadata = {
        'file_name': '%s.html' % (meta['id'],)
    }
    meta.update(metadata)
    print(html_file)
    result = api.ingest_upload(collection_id, Path(html_file), meta)
    document_id = result.get('id')
    print(document_id)
    cleaned_name = meta['author'].replace('Gemeente ', '')
    if cleaned_name in gemeenten:
        print(gemeenten[cleaned_name])
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
if len(document_links) > 0:
    # Turn the two proxies into JSON form:
    entities = [l.to_dict() for l in document_links]

    # You can also feed an iterator to write_entities if you
    # want to upload a very large
    api.write_entities(collection_id, entities)
