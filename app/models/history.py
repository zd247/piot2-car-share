import datetime
from datetime import *
from dateutil.tz import *
from app import db


class History(db.Model):
    __tablename__ = 'history'
    email = db.Column(db.String(255), nullable=False, unique=True, primary_key=True)
    car = db.Column(db.String(100), nullable=False, unique=True)
    event_id = db.Column(db.String(255), nullable=False, unique=True)
    rent_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    verify_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, car, rent_date, return_date):
        self.email = email
        self.car = car
        self.rent_date = rent_date
        self.return_date = return_date
        self.verify_date = datetime.now()