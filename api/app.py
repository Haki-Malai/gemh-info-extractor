from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from apifairy import APIFairy

db = SQLAlchemy()
apifairy = APIFairy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Disable trailing slash
    app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)
    apifairy.init_app(app)

    # Register click commands
    from api.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    @app.route("/")
    def index():
        return "Hello World!"

    return app
