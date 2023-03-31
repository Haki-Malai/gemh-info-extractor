from flask import Flask, redirect, url_for, request
from config import Config
 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.route("/")
    def index():
        return "Hello World!"

    return app
