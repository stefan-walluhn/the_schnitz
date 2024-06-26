import click
import uuid

from flask import current_app
from flask.cli import FlaskGroup

from the_schnitz.app import create_app, rabbitmq_channel
from the_schnitz.rabbitmq import RabbitMQConsumer
from the_schnitz.callbacks import AudioCallback


class QueueParamType(click.ParamType):
    name = 'queue'

    def convert(self, value, param, ctx):
        return f"{value}-{str(uuid.uuid4())}"


QUEUE = QueueParamType()


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command('log_client')
@click.option('-q', '--queue', default="log")
def log_client(queue):
    while True:
        client = RabbitMQConsumer(
            rabbitmq_channel,
            current_app.config['RABBITMQ_EXCHANGE'],
            queue,
            print
        )

        client.subscribe()
        current_app.logger.error('Connection lost, try to reconnect')


@cli.command('audio_client')
@click.option('-q', '--queue', default="audio", type=QUEUE)
@click.option('-f', '--audio-file', required=True)
def audio_client(queue, audio_file):
    while True:
        client = RabbitMQConsumer(
            rabbitmq_channel,
            current_app.config['RABBITMQ_EXCHANGE'],
            queue,
            AudioCallback(audio_file),
            exclusive=True)

        client.subscribe()
        current_app.logger.error('Connection lost, try to reconnect')
