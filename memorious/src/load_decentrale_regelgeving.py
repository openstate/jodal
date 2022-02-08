from glob import glob
from os.path import basename, splitext
import json
from pathlib import Path

# Import alephclient:
from alephclient.api import AlephAPI

def load_meta(f):
    result = None
    with open(f, 'r') as in_file:
        result = json.load(in_file)
    return result

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
    print(html_file)
    result = api.ingest_upload(collection_id, Path(html_file), metadata)
    document_id = result.get('id')
    print(document_id)
    cleaned_name = meta['author'].replace('Gemeente ', '')
    if cleaned_name in gemeenten:
        print(gemeenten[cleaned_name])
    # file_path = 'www.personadeinteres.org/uploads/example.pdf'
    # metadata = {'file_name': 'example.pdf'}
    # # Upload the document:
    # result = api.ingest_upload(collection_id, file_path, metadata)
    #
    # # Finally, we have an entity ID:
    # document_id = result.get('id')
