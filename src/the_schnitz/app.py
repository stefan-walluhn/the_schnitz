import os
import pika
import redis

from flask import Flask, current_app, g
from werkzeug.local import LocalProxy

from the_schnitz.repository import ConfigRepository, RedisRepository
from the_schnitz.rabbitmq import RabbitMQProducer
from the_schnitz.schema import LocationSchema
from the_schnitz.services import LocationService


def get_location_schema():
    if 'location_schema' not in g:
        g.location_schema = LocationSchema()

    return g.location_schema


def get_config_repository():
    if 'config_repository' not in g:
        current_app.logger.debug('creating config repository')
        g.config_repository = ConfigRepository(current_app.config['LOCATIONS'])

    return g.config_repository


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


def get_rabbitmq_connection():
    if 'rabbitmq_connection' not in g:
        current_app.logger.debug('establish rabbitmq connection')
        g.rabbitmq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=current_app.config['RABBITMQ_HOST']
            )
        )

    return g.rabbitmq_connection


def close_rabbitmq_connection():
    connection = g.pop('rabbitmq_connection', None)

    if connection is not None:
        current_app.logger.debug('close rabbitmq connection')
        connection.close()


def get_rabbitmq_channel():
    if 'rabbitmq_channel' not in g:
        current_app.logger.debug('establish rabbitmq channel')
        g.rabbitmq_channel = get_rabbitmq_connection().channel()

    return g.rabbitmq_channel


def get_rabbitmq_producer():
    if 'rabbitmq_producer' not in g:
        current_app.logger.debug('creating rabbitmq producer')
        g.rabbitmq_producer = RabbitMQProducer(
            get_rabbitmq_channel(),
            current_app.config['RABBITMQ_EXCHANGE']
        )

    return g.rabbitmq_producer


def get_location_service():
    if 'location_service' not in g:
        current_app.logger.debug('creating location service')
        g.location_service = LocationService(
            get_config_repository(),
            get_redis_repository(),
            get_rabbitmq_producer()
        )

    return g.location_service


def create_app():
    from the_schnitz.config_loader import locations
    from the_schnitz.views import discovery

    app = Flask(__name__)
    app.config.from_object('the_schnitz.default_config')
    app.config.from_file(os.path.join(os.getcwd(), 'locations.yml'),
                         load=locations.load)

    @app.teardown_appcontext
    def teardown_rabbitmq(e):
        close_rabbitmq_connection()

    app.register_blueprint(discovery.bp)

    return app


location_schema = LocalProxy(get_location_schema)
location_service = LocalProxy(get_location_service)
rabbitmq_channel = LocalProxy(get_rabbitmq_channel)
