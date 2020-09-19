import datetime
from datetime import *
from dateutil.tz import *
from app import app, db, gcalendar_service


class History(db.Model):
    __tablename__ = 'history'
    email = Column(String(255), nullable=False, unique=True, primary_key=True)
    car = Column(String(100), primary_key=True,
                      nullable=False, unique=True)
    rent_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    verify_date = Column(DateTime, nullable=False)

    def __init__(self, email, car, rent_date, return_date):
        self.email = email
        self.car = car
        self.rent_date = rent_date
        self.return_date = return_date
        self.verify_date = datetime.now()