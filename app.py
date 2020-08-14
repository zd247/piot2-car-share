from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# pre-config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
db = SQLAlchemy(app)

# models
class Car(db.Model):
    # TODO: convert to enum for value that has less than 10 attributes.
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    make = db.Column(db.String(100), nullable = False)
    body = db.Column(db.String(100), nullable = False)
    colour = db.Column(db.String(30), nullable = False)
    seats = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String(100), nullable = False)
    cost_per_hour = db.Column(db.Float, nullable = False)
    manu_date = db.Column(db.DateTime, nullable = False, default= datetime.utcnow)
    
    
    def __repr__(self):
        return 'Car data' + str(self.id)
    
    
    
# routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars', methods =['GET', 'POST'])
def cars():
    if request.method == 'POST':
        car_name = request.form['name']
        car_make = request.form['make']
        car_body = request.form['body']
        car_colour = request.form['colour']
        car_seats = request.form['seats']
        car_location = request.form['location']
        car_cost_per_hour = request.form['cost_per_hour']
        
        new_car = Car(name = car_name,
                        make = car_make,
                         body = car_body,
                          colour = car_colour,
                           seats = car_seats,
                            location = car_seats,
                             cost_per_hour = car_cost_per_hour)
        
        
        # saving to database
        db.session.add(new_car)
        db.session.commit()
        
        return redirect('/cars')
    else: 
        all_cars = Car.query.order_by(Car.manu_date).all()
        return render_template('cars.html', cars = all_cars)
    

@app.route('/cars/delete/<int:id>')
def delete(id):
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return redirect('/cars')

@app.route('/cars/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    car = Car.query.get_or_404(id)
    
    if request.method == 'POST':
        car.name = request.form['name']
        car.make = request.form['make']
        car.body = request.form['body']
        car.colour = request.form['colour']
        car.seats = request.form['seats']
        car.location = request.form['location']
        car.cost_per_hour = request.form['cost_per_hour']
        car.manu_date = request.form['car_manu_date']
        db.session.commit()
        
        return redirect('/cars')
    else:
        return render_template('edit.html', car = car)
    
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)    