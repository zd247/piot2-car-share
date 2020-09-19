import os
import datetime

from flask import Flask, request, render_template_string, render_template, jsonify, make_response, session, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_restplus import Api

from app.cloud import * 
from app._google import create_service


# init app and cors
app = Flask(__name__, instance_relative_config=True)

# security
CORS(app)

bcrypt = Bcrypt(app) 
jwt = JWTManager(app)

api = Api()
jwt._set_error_handler_callbacks(api)

blacklist = set()

# will be called whenever create_access_token is used.
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user['role']}

@jwt.user_identity_loader
def user_identity_lookup(identity):
    return identity

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist



# load config setting from env config files
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# declare SQLAlchemy 
# db = init_connection_engine() # declare the cloud database connection
db = SQLAlchemy(app)


# Register Google APIs
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
# calls will be like this: https://www.googleapis.com/auth/calendar/v3/[your-resources-services], method: [POST,GET,..]

gcalendar_service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


# Register email with gmail service
import smtplib

mail_server = smtplib.SMTP("smtp.gmail.com", 587) 
mail_server.starttls() # listening to gmail server
gmail_account = "zduy2407@gmail.com"
mail_server.login("zduy2407@gmail.com", "Game1468")


# register controller blueprints
from app.apis.auth_method import auth_blueprint
from app.apis.cars_method import cars_blueprint
from app.apis.users_method import users_blueprint
from app.apis.bookings_method import bookings_blueprint
from app.apis.emails_method import emails_blueprint
from app.models.car import Car
from app.models.user import User
from sqlalchemy import exc, extract
from sqlalchemy.sql.functions import count, Cast, func
import json
import re

app.register_blueprint(auth_blueprint)
app.register_blueprint(cars_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(bookings_blueprint)
app.register_blueprint(emails_blueprint)


# Registering html routes here
@app.route('/')
def index():
    return render_template("index.html")


@app.route("/convert_to_json", methods=["POST"])
def convert_to_json():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res

#TODO
# store the access token in browswer cookie

# when an app.route(...) function is fetched, get the access token from the browswer cookie

# there are two ways to work on the access token

# fetch the api/v1 routes with authorization access token passed, if returned request error, display an alert box


//TODO move history to another directory
# class History(db.Model):
#     __tablename__ = 'history'
#     email = Column(String(255), nullable=False, unique=True, primary_key=True)
#     car = Column(String(100), primary_key=True,
#                       nullable=False, unique=True)
#     rent_date = Column(DateTime, nullable=False)
#     return_date = Column(DateTime, nullable=False)
#     verify_date = Column(DateTime, nullable=False)

#     def __init__(self, email, car, rent_date, return_date):
#         self.email = email
#         self.car = car
#         self.rent_date = rent_date
#         self.return_date = return_date
#         self.verify_date = datetime.now()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customer/home')
def customer_home():
    return render_template('customer/home.html')


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
        return render_template('customer/booking.html',email=email, car_name=name)
    else:
        rent_date = request.form['rent_date']
        return_date = request.form['return_date']
        if datetime.strptime(rent_date, '%Y-%m-%d') > datetime.today() or datetime.strptime(rent_date, '%Y-%m-%d') > datetime.strptime(return_date, '%Y-%m-%d'):
            return render_template('customer/booking.html',msg='Invalid date',email=email, car_name=name)
        else:
            db.session.add(History(email, name, rent_date, return_date))
            db.session.commit()
    return redirect(url_for('customer_home'))

@app.route('/admin/home')
def admin_home():
    return render_template('admin/home.html')

@app.route('/admin/user', methods=['GET', 'POST'])
def admin_user():
    if request.method == 'POST':
        try:
            new_list = request.form['user_data']
            User.query.delete()
            for user in json.loads(new_list):
                db.session.add(User(
                    user['email'], user['password'], user['first_name'], user['last_name'], user['role']))
        except exc.SQLAlchemyError as e:
            db.session.rollback()
    db.session.commit()
    list = User.query.all()
    user_schema = UserSchema(many=True)
    user_list = user_schema.dump(list)
    return render_template('admin/user.html', user_list=user_list)

@app.route('/admin/car', methods=['GET', 'POST'])
def admin_car():
    if request.method == 'POST':
        try:
            new_list = request.form['car_data']
            Car.query.delete()
            for car in json.loads(new_list):
                db.session.add(Car(car['name'], car['make'], car['body'], car['colour'],
                                      car['seats'], car['location'], car['cost_per_hour'], car['manu_date']))
        except exc.SQLAlchemyError as e:
            db.session.rollback()
    db.session.commit()
    list = Car.query.all()
    car_schema = CarSchema(many=True)
    car_list = car_schema.dump(list)
    return render_template('admin/car.html', car_list=car_list)

@app.route('/engineer/home')
def engineer_home():
    return render_template('engineer/home.html')

@app.route('/manager/home')
def manager_home():
    return render_template('manager/home.html')

@app.route('/manager/customer')
def manager_customer():
    new_customer_in_6_month = db.session.query(Cast(extract('month', User.email_confirmed_at), String), func.count(User.email)).group_by(extract('month', User.email_confirmed_at)).all()
    car_by_make = db.session.query(Car.make, func.count(Car.name)).group_by(Car.make).all()
    return render_template('manager/customer.html', new_customer_in_6_month=json.dumps(new_customer_in_6_month)
                                        ,   car_by_make=json.dumps(car_by_make))

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
        # Check if account exists using db
        account = User.query.filter_by(email=email).first()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z]+', fname) or not re.match(r'[A-Za-z]+', lname):
            msg = 'Fiest name and last name must contain only characters!'
        elif not fname or not lname or not password or not email:
            msg = 'Please fill out the form!'
        else:
            db.session.add(User(email, password, fname, lname, role.lower()))
            db.session.commit()
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