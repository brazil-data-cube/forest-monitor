import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from forest_monitor.blueprint import blueprint
from forest_monitor.config import get_settings

flask_bcrypt = Bcrypt()


def create_app(config):
    app = Flask(__name__)

    with app.app_context():
        app.config.from_object(config)
        app.register_blueprint(blueprint)
        flask_bcrypt.init_app(app)

    return app

app = create_app(get_settings(os.environ.get('ENVIRONMENT', 'DevelopmentConfig')))

CORS(app, resorces={r'/d/*': {"origins": '*'}})