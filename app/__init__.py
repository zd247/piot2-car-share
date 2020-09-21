import os
import datetime

from flask import Flask, request, render_template_string, render_template, jsonify, make_response, session, redirect, url_for, Response
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_restplus import Api

from app.cloud import * 
from app._google import create_service
from flask_marshmallow import Marshmallow

import requests
import json
import os
import time



# init app and cors
app = Flask(__name__, instance_relative_config=True)
ma = Marshmallow(app)

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

app.register_blueprint(auth_blueprint)
app.register_blueprint(cars_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(bookings_blueprint)
app.register_blueprint(emails_blueprint)


#===================[Routing]========================


API_ROUTE = 'http://127.0.0.1:5000/api/v1/'

@app.route('/')
def index():
    return render_template('index.html')

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/login_redirect')
def login_redirect():
    role = request.cookies.get('role')
    if (role == 'customer'):
        return redirect(url_for('customer_home'))
    elif role == 'admin':
        return redirect(url_for('admin_home'))
    return url_for('login')


@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    # session.pop('id', None)
    session.pop('email', None)
    session.clear()
    
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('access_token')
    resp.delete_cookie('email')
    resp.delete_cookie('role')
    resp.delete_cookie('first_name')
    resp.delete_cookie('last_name')
    
    return resp

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# ==============[customers]===============

@app.route('/customer/home')
def customer_home():
    return render_template('customer/home.html')

@app.route('/customer/car')
def customer_car():
    car_list = Car.query.all()
    first_name = request.cookies.get('first_name')
    last_name = request.cookies.get('last_name')
    return render_template('customer/car.html', car_list=car_list, name= first_name + ' ' + last_name)

@app.route('/customer/booking/', methods=['GET', 'POST'])
def customer_booking():   
    # if request.method == 'POST':
    #     try:
            
    #     except Exception as e:
    #         print (e)
    return render_template('customer/booking.html')

from app.models.history import History

@app.route('/customer/history')
def customer_history():
    customer_email = request.cookies.get('email')
    history_list = History.query.filter_by(email=customer_email).all()
    return render_template('customer/history.html', history_list=history_list)

#================[Admin]=================

class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'email_confirmed_at', 'password',
            'registered_on', 'first_name', 'last_name', 'active', 'role')

@app.route('/admin/home')
def admin_home():
    return render_template('admin/home.html')

@app.route('/admin/user', methods=['GET', 'POST'])
def admin_user():
    user_list = User.query.all()
    return render_template('admin/user.html', user_list=user_list)

@app.route('/admin/car', methods=['GET', 'POST'])
def admin_car():
    car_list = Car.query.all()
    return render_template('admin/car.html', car_list=car_list)

# @app.route('/engineer/home')
# def engineer_home():
#     return render_template('engineer/home.html')

# @app.route('/manager/home')
# def manager_home():
#     return render_template('manager/home.html')

# @app.route('/manager/customer')
# def manager_customer():
#     new_customer_in_6_month = db.session.query(Cast(extract('month', User.email_confirmed_at), String), func.count(User.email)).group_by(extract('month', User.email_confirmed_at)).all()
#     car_by_make = db.session.query(Car.make, func.count(Car.name)).group_by(Car.make).all()
#     return render_template('manager/customer.html', new_customer_in_6_month=json.dumps(new_customer_in_6_month)
#                                         ,   car_by_make=json.dumps(car_by_make))




