import click
import pika

from msgpack import packb

from the_schnitz.rabbitmq import RabbitMQConsumer, RabbitMQProducer
from the_schnitz.callbacks import MessagePackCallback, AudioCallback


@click.command()
@click.option('-h', '--host', default="localhost")
@click.option('-e', '--exchange', default="discoveries")
@click.option('-q', '--queue', default="telegram")
def log_client(host, exchange, queue):
    client = RabbitMQConsumer(host, exchange, queue, MessagePackCallback(print))
    client.subscribe()


@click.command()
@click.option('-h', '--host', default="localhost")
@click.option('-e', '--exchange', default="discoveries")
@click.option('-q', '--queue', default="audio")
@click.option('-f', '--audio-file', required=True)
def audio_client(host, exchange, queue, audio_file):
    client = RabbitMQConsumer(host, exchange, queue,
                            MessagePackCallback(AudioCallback(audio_file)))
    client.subscribe()


@click.command()
@click.option('-h', '--host', default="localhost")
@click.option('-e', '--exchange', default="discoveries")
def test_it(host, exchange):
    data = {'text': 'test message'}
    producer = RabbitMQProducer(host, exchange)

    producer.publish(packb(data))
