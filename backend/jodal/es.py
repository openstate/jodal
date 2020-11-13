import json
import logging

from elasticsearch import Elasticsearch, serializer, compat, exceptions

es = None


class JSONSerializerPython2(serializer.JSONSerializer):
    """Override elasticsearch library serializer to ensure it encodes utf characters during json dump.
    See original at: https://github.com/elastic/elasticsearch-py/blob/master/elasticsearch/serializer.py#L42
    A description of how ensure_ascii encodes unicode characters to ensure they can be sent across the wire
    as ascii can be found here: https://docs.python.org/2/library/json.html#basic-usage
    """

    def dumps(self, data):
        # don't serialize strings
        if isinstance(data, compat.string_types):
            return data
        try:
            return json.dumps(data, default=self.default, ensure_ascii=True)
        except (ValueError, TypeError) as e:
            raise exceptions.SerializationError(data, e)


def setup_elasticsearch(config={}):
    """
    Set up a connection to Elasticsearch and returns the instance.
    """

    global es

    if es is None:
        logging.info(
            'Setting up Elasticsearch: %s' % (
                config['jodal']['elasticsearch'],))
        es = Elasticsearch(
            [config['jodal']['elasticsearch']],
            serializer=JSONSerializerPython2())
    return es
