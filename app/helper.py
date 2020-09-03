from flask.cli import with_appcontext
from app import db
from app.models.car import Car


@with_appcontext
def seed():
   """Seed the database."""
   car1 = Car("Honda", "Sedan", "Silver", "White",4, "NYC", 15.5, "2018-12-19 09:26:03.478039")
   car2 = Car("Subaru", "Truck", "Yellow", "White",7, "BC", 23.5, "2018-12-20 09:26:03.478039")
   db.session.add_all([car1, car2])
   db.session.commit()