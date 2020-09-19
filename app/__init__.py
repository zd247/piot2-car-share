import os
import datetime

from flask import Flask, request, render_template_string, render_template, jsonify, make_response
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