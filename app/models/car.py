import datetime
from app import app, db

class Car(db.Model):
    """ Car Model for storing car related details """
    
    __tablename__ = "cars"
    
    name = db.Column(db.String(100), primary_key = True, nullable = False)
    make = db.Column(db.String(100), nullable = False)
    body = db.Column(db.String(100), nullable = False)
    colour = db.Column(db.String(30), nullable = False)
    seats = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String(100), nullable = False)
    cost_per_hour = db.Column(db.Float, nullable = False)
    manu_date = db.Column(db.DateTime, nullable = True)
    
    def __init__(self, name, make, body, colour, seats, location, cost_per_hour, manu_date):
        self.name = name
        self.make = make
        self.body = body
        self.colour = colour
        self.seats = seats
        self.location = location
        self.cost_per_hour = cost_per_hour
        self.manu_date = manu_date
        
