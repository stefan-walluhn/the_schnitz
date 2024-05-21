from flask import Flask
from msgpack import packb

from the_schnitz.rabbitmq import RabbitMQProducer

app = Flask(__name__)
app.config.from_object('the_schnitz.default_config')

@app.route("/")
def publish():
    data = {'route': 'publish'}
    producer = RabbitMQProducer(app.config['RABBITMQ_HOST'],
                                app.config['RABBITMQ_EXCHANGE'])

    producer.publish(packb(data))

    return "<p>Hello, World!</p>"
