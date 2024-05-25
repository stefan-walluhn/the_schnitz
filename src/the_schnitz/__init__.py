import redis

from flask import current_app, g

from the_schnitz.repository import RedisRepository
from the_schnitz.schema import LocationSchema


def get_redis_client():
    if 'redis_client' not in g:
        current_app.logger.debug('creating redis client')
        g.redis_client = redis.Redis(decode_responses=True)  # XXX parameterize

    return g.redis_client


def get_redis_repository():
    if 'redis_repository' not in g:
        current_app.logger.debug('creating redis repository')
        g.redis_repository = RedisRepository(get_redis_client())

    return g.redis_repository


def get_location_schema():
    if 'location_schema' not in g:
        g.location_schema = LocationSchema()

    return g.location_schema
