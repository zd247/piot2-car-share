import datetime
from datetime import *
from dateutil.tz import *
from app import app, db, gcalendar_service

class Car(db.Model):
    """ Car Model for storing car related details """
    
    __tablename__ = "cars"
    
    name = db.Column(db.String(100), primary_key = True, nullable = False, unique=True)
    make = db.Column(db.String(100), nullable = False)
    body = db.Column(db.String(100), nullable = False)
    colour = db.Column(db.String(30), nullable = False)
    seats = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String(100), nullable = False)
    cost_per_hour = db.Column(db.Float, nullable = False)
    manu_date = db.Column(db.DateTime, nullable = True)
    calendar_id = db.Column(db.String(255), nullable = False, unique=True)
    status = db.Column(db.String(20), db.CheckConstraint('status="Available" or status="Unavailable"'))

    
    def __init__(self, name, make, body, colour, seats, location, cost_per_hour, manu_date, calendar_id="", status="Available"):
        self.name = name
        self.make = make
        self.body = body
        self.colour = colour
        self.seats = seats
        self.location = location
        self.cost_per_hour = cost_per_hour
        self.manu_date = manu_date
        self.status = status
        
        if calendar_id == "":
        # Calendar
            calendar_body = {
                'summary': self.name,
                'timeZone': datetime.now(tzlocal()).tzname()
            }
            created_calendar = gcalendar_service.calendars().insert(body = calendar_body).execute()
            
            self.calendar_id = created_calendar['id']
        else:
            self.calendar_id = calendar_id
        
