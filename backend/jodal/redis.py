import json
import logging

from redis import Redis

redis_client = None

def setup_redis(config={}):
    global redis_client

    if redis_client is None:
        redis_config = config['jodal']['redis']
        print(redis_config)
        redis_client = Redis(**redis_config)

    return redis_client
