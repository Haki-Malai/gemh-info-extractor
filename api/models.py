from datetime import datetime

from api.app import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    gemh = db.Column(db.String(64), index=True, unique=True)
    website = db.Column(db.String(128), index=True, unique=True)
    registration_date = db.Column(db.DateTime, index=True,
                                  default=datetime.utcnow)

    def __repr__(self):
        return '<Company %s>' % self.name
