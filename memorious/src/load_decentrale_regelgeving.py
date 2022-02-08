from glob import glob

# Import alephclient:
from alephclient.api import AlephAPI

# By default, alephclient will read host and API key from the
# environment. You can also pass both as an argument here:
api = AlephAPI()

# Get the collection (dataset)
foreign_id = 'decentrale_regelgeving_xml'
data_path = '/data/results/decentrale_regelgeving'
collection = api.load_collection_by_foreign_id(foreign_id)
collection_id = collection.get('id')

entities = api.stream_entities(collection, schema='PublicBody')
for e in entities:
    print(e)

for f in glob('%s/*.json' % (data_path,)):
    print(f)
# file_path = 'www.personadeinteres.org/uploads/example.pdf'
# metadata = {'file_name': 'example.pdf'}
# # Upload the document:
# result = api.ingest_upload(collection_id, file_path, metadata)
#
# # Finally, we have an entity ID:
# document_id = result.get('id')
