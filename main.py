import os
from api import create_app

app = create_app(os.getenv('FLASK_CONFIG'))

with app.app_context():
    from api import models, db
    db.create_all()