import os

from flask import Flask

from the_schnitz.config_loader import locations
from the_schnitz.rabbitmq import init_rabbitmq
from the_schnitz.views import discovery


def create_app():
    app = Flask(__name__)
    app.config.from_object('the_schnitz.default_config')
    app.config.from_file(os.path.join(os.getcwd(), 'locations.yml'), load=locations.load)

    init_rabbitmq(app)

    app.register_blueprint(discovery.bp)

    return app
