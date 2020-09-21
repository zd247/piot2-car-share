from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, CheckConstraint, exc, DateTime, Boolean, extract
from datetime import datetime
from flask_marshmallow import Marshmallow
from sqlalchemy.sql.functions import count, Cast, func
import re
import json

# Enter your database connection details below
app = Flask(__name__)
app.secret_key = 'root'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:raspberry@localhost/database'
mysql = SQLAlchemy(app)
ma = Marshmallow(app)


class History(mysql.Model):
    __tablename__ = 'history'
    email = Column(String(255), nullable=False, unique=True, primary_key=True)
    car = Column(String(100), primary_key=True, nullable=False, unique=True)
    rent_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    verify_date = Column(DateTime, primary_key=True, nullable=False)

    def __init__(self, email, car, rent_date, return_date):
        self.email = email
        self.car = car
        self.rent_date = rent_date
        self.return_date = return_date
        self.verify_date = datetime.now()


class User(mysql.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    email = Column(String(255), nullable=False, unique=True, primary_key=True)
    email_confirmed_at = Column(DateTime())
    password = Column(String(255), nullable=False, server_default='')
    registered_on = Column(DateTime, nullable=False)

    # User information
    first_name = Column(String(100), nullable=False, server_default='')
    last_name = Column(String(100), nullable=False, server_default='')

    active = Column('is_active', Boolean(), nullable=False, server_default='1')

    # roles = relationship('Role', secondary='user_roles')
    role = Column(String(30), nullable=False, server_default='user')

    def __init__(self, email, password, first_name, last_name, role, email_confirmed_at=datetime.now(), registered_on=datetime.now(), active=True):
        self.email = email
        self.email_confirmed_at = email_confirmed_at
        self.password = password
        self.registered_on = registered_on
        self.first_name = first_name
        self.last_name = last_name
        self.active = active
        self.role = role


class Car(mysql.Model):
    """ Car Model for storing car related details """

    __tablename__ = "cars"

    name = Column(String(100), primary_key=True, nullable=False, unique=True)
    make = Column(String(100), nullable=False)
    body = Column(String(100), nullable=False)
    colour = Column(String(30), nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String(100), nullable=False)
    cost_per_hour = Column(Float, nullable=False)
    manu_date = Column(DateTime, nullable=True)
    calendar_id = Column(String(255), nullable=False, unique=True)
    status = Column(String(20), CheckConstraint(
        'status="Available" or status="Unavailable"'))

    def __init__(self, name, make, body, colour, seats, location, cost_per_hour, manu_date, calendar_id="created calendar", status="Available"):
        self.name = name
        self.make = make
        self.body = body
        self.colour = colour
        self.seats = seats
        self.location = location
        self.cost_per_hour = cost_per_hour
        self.manu_date = manu_date
        self.calendar_id = calendar_id
        self.status = status


class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'email_confirmed_at', 'password',
                  'registered_on', 'first_name', 'last_name', 'active', 'role')


class CarSchema(ma.Schema):
    class Meta:
        fields = ('name', 'make', 'body', 'colour', 'seats',
                  'location', 'cost_per_hour', 'manu_date', 'calendar_id', 'status')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/customer/cancel')
def customer_cancel():
    email = session['email']
    history = History.query.filter(History.return_date>=datetime.now()).filter_by(email=email).first()
    booked_car = Car.query.filter_by(name=history.car).first()
    booked_car.status = 'Available'
    mysql.session.commit()
    return redirect(url_for('customer_home'))

@app.route('/customer/home')
def customer_home():
    msg = ""
    email = session['email']
    history = History.query.filter(History.return_date>=datetime.now()).filter_by(email=email).first()
    if history:
        booked_car = Car.query.filter_by(name=history.car).first()
        if booked_car.status == 'Unavailable':
            msg = "You are currently booking " + booked_car.name + " until " + history.return_date.strftime('%d/%m/%Y')
    return render_template('customer/home.html', email=email, msg=msg)


@app.route('/customer/car')
def customer_car():
    car_list = Car.query.all()
    return render_template('customer/car.html', car_list=car_list)


@app.route('/customer/booking/<name>', methods=['GET', 'POST'])
def customer_booking(name):
    # print(name)
    email = session['email']
    # return render_template('customer/booking.html')
    if request.method == 'GET':
        return render_template('customer/booking.html', email=email, car_name=name)
    else:
        rent_date = request.form['rent_date']
        return_date = request.form['return_date']
        if datetime.strptime(rent_date, '%Y-%m-%d') > datetime.today() or datetime.strptime(rent_date, '%Y-%m-%d') > datetime.strptime(return_date, '%Y-%m-%d'):
            return render_template('customer/booking.html', msg='Invalid date', email=email, car_name=name)
        else:
            mysql.session.add(History(email, name, rent_date, return_date))
            booked_car = Car.query.filter_by(name=name).first()
            booked_car.status = "Unavailable"
            mysql.session.commit()
    return redirect(url_for('customer_home'))


@app.route('/customer/history')
def customer_history():
    history_list = History.query.filter_by(email=session['email']).all()
    return render_template('customer/history.html', history_list=history_list)


@app.route('/admin/home')
def admin_home():
    email = session['email']
    return render_template('admin/home.html',email=email)


@app.route('/admin/user', methods=['GET', 'POST'])
def admin_user():
    if request.method == 'POST':
        try:
            new_list = request.form['user_data']
            User.query.delete()
            for user in json.loads(new_list):
                mysql.session.add(User(
                    user['email'], user['password'], user['first_name'], user['last_name'], user['role'], user['email_confirmed_at'], user['registered_on'], user['active']))
        except exc.SQLAlchemyError as e:
            mysql.session.rollback()
    mysql.session.commit()
    list = User.query.all()
    user_schema = UserSchema(many=True)
    user_list = user_schema.dump(list)
    return render_template('admin/user.html', user_list=user_list)


@app.route('/admin/car', methods=['GET', 'POST'])
def admin_car():
    if request.method == 'POST':
        try:
            new_list = request.form['car_data']
            print(new_list)
            Car.query.delete()
            for car in json.loads(new_list):
                mysql.session.add(Car(car['name'], car['make'], car['body'], car['colour'],
                                      car['seats'], car['location'], car['cost_per_hour'], car['manu_date'].replace('T', ' '), car['calendar_id'], car['status']))
        except exc.SQLAlchemyError as e:
            mysql.session.rollback()
    mysql.session.commit()
    list = Car.query.all()
    car_schema = CarSchema(many=True)
    car_list = car_schema.dump(list)
    return render_template('admin/car.html', car_list=car_list)


@app.route('/admin/history')
def admin_history():
    history_list = History.query.all()
    return render_template('admin/history.html', history_list=history_list)


@app.route('/engineer/home')
def engineer_home():
    email = session['email']
    return render_template('engineer/home.html',email=email)


@app.route('/manager/home')
def manager_home():
    email = session['email']
    return render_template('manager/home.html',email=email)


@app.route('/manager/customer')
def manager_customer():
    new_customer_in_6_month = mysql.session.query(Cast(extract('month', User.email_confirmed_at), String), func.count(
        User.email)).filter_by(role='customer').group_by(extract('month', User.email_confirmed_at)).all()
    customer_booking_in_6_month = mysql.session.query(Cast(extract('month', History.verify_date), String), func.count(
        History.email)).group_by(extract('month', History.verify_date)).all()
    return render_template('manager/customer.html', new_customer_in_6_month=json.dumps(new_customer_in_6_month),
                           customer_booking_in_6_month=json.dumps(customer_booking_in_6_month))


@app.route('/manager/car')
def manager_car():
    car_by_make = mysql.session.query(
        Car.make, func.count(Car.name)).group_by(Car.make).all()
    car_make_booked = mysql.session.query(Car.make, func.count(
        Car.make)).join(History, Car.name == History.car).group_by(Car.make).all()
    return render_template('manager/car.html', car_by_make=json.dumps(car_by_make), car_make_booked=json.dumps(car_make_booked))



@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']

        account = User.query.filter_by(email=email, password=password).first()

        # If account exists in accounts table in out database
        if (account):
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account.email
            session['role'] = account.role
            # Redirect to home page
            # template = account.role.lower() + '/home.html'
            template = account.role.lower() + '_home'
            # return render_template(template, email=session['email'])
            return redirect(url_for(template))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect Email/password!'

    return render_template('login.html', msg=msg)

# http://localhost:5000/login/logout - this will be the logout page


@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
#    session.pop('id', None)
    session.pop('email', None)
    # Redirect to login page
    #  return redirect(url_for('login'))
    return redirect(url_for('index'))

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'password' in request.form and 'email' in request.form and 'birth' in request.form:
        # Create variables for easy access
        fname = request.form['fname']
        lname = request.form['lname']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        # Check if account exists using MySQL
        account = User.query.filter_by(email=email).first()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z]+', fname) or not re.match(r'[A-Za-z]+', lname):
            msg = 'Fiest name and last name must contain only characters!'
        elif not fname or not lname or not password or not email:
            msg = 'Please fill out the form!'
        else:
            mysql.session.add(
                User(email, password, fname, lname, role.lower()))
            mysql.session.commit()
            # msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
