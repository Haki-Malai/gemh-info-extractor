from flask import Flask, redirect, url_for
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from apifairy import APIFairy
from redis import Redis

db = SQLAlchemy()
mg = Migrate()
ma = Marshmallow()
apifairy = APIFairy()
redis_client = Redis(host=config['default'].REDIS_HOST, port=6379)


def create_app(config_name: str) -> Flask:
    """Create a Flask application using the app factory pattern.
    :param config_name: The configuration to use.
    :return: The Flask application.
    """
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])

    # Disable trailing slash
    app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)
    mg.init_app(app, db)
    ma.init_app(app)
    apifairy.init_app(app)

    # Register click commands
    from api.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    # Register error handlers
    from api.errors import bp as error_bp
    app.register_blueprint(error_bp)

    # Register blueprints
    from api.company import bp as company_bp
    app.register_blueprint(company_bp)

    # Register shell context
    from api import models

    @app.shell_context_processor
    def make_shell_context() -> dict:
        ctx = {'db': db}
        for attr in dir(models):
            model = getattr(models, attr)
            if hasattr(model, '__bases__') and \
                    db.Model in getattr(model, '__bases__'):
                ctx[attr] = model
        return ctx

    # Redirect to API docs
    @app.route('/')
    def index():
        return redirect(url_for('apifairy.docs'))

    return app
