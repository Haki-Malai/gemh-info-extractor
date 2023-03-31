import os
from api.app import create_app

app = create_app(os.getenv('FLASK_CONFIG'))

with app.app_context():
    from api.app import db
    from api import models

    db.create_all()
