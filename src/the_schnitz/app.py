from flask import Flask
from msgpack import packb

from the_schnitz.rabbitmq import init_rabbitmq, get_rabbitmq_producer

def create_app():
    app = Flask(__name__)
    app.config.from_object('the_schnitz.default_config')

    app = init_rabbitmq(app)

    @app.route("/")
    def publish():
        data = {'route': 'publish'}
        producer = get_rabbitmq_producer()
        producer.publish(packb(data))

        return "<p>Hello, World!</p>"

    return app
