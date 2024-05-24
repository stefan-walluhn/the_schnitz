import pika

from flask import current_app, g


def get_rabbitmq_connection():
    if 'rabbitmq_connection' not in g:
        current_app.logger.debug('establish rabbitmq connection')
        g.rabbitmq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=current_app.config['RABBITMQ_HOST']
            )
        )

    return g.rabbitmq_connection


def close_rabbitmq_connection(e=None):
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


def init_rabbitmq(app):
    app.teardown_appcontext(close_rabbitmq_connection)
    return app


class RabbitMQProducer:
    def __init__(self, channel, exchange):
        self.channel = channel
        self.exchange = exchange

        self.channel.exchange_declare(exchange=self.exchange,
                                      exchange_type='fanout')

    def publish(self, data):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key="",
                                   body=data)


class RabbitMQConsumer:
    def __init__(self, channel, exchange, queue, callback):
        self.callback = callback

        self.channel = channel
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type='fanout')

        self.channel.queue_declare(queue=queue, exclusive=True)
        self.channel.queue_bind(exchange=exchange, queue=queue)

        self.channel.basic_consume(queue=queue,
                                   on_message_callback=self.__callback__,
                                   auto_ack=True)

    def subscribe(self):
        self.channel.start_consuming()

    def __callback__(self, ch, method, properties, body):
        current_app.logger.debug('consumung message')
        self.callback(body)
