import os
import datetime

from flask import Flask, request, render_template_string
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

# register controller blueprints
from app.apis.auth_method import auth_blueprint
from app.apis.cars_method import cars_blueprint
from app.apis.users_method import users_blueprint
from app.apis.bookings_method import bookings_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(cars_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(bookings_blueprint)



