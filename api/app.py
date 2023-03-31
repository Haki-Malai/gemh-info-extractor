from flask import Flask, redirect, url_for, request
from config import config
 

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Disable trailing slash
    app.url_map.strict_slashes = False

    @app.route("/")
    def index():
        return "Hello World!"

    return app
