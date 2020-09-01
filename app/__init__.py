import os
import datetime

from flask import Flask, request, render_template_string
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_babelex import Babel

from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt


# init app and cors
app = Flask(__name__, instance_relative_config=True)

# security
CORS(app)
babel = Babel(app)

bcrypt = Bcrypt(app) 
jwt = JWTManager(app)

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
db = SQLAlchemy(app) 

# register controller blueprints
from app.apis.auth_method import auth_blueprint
from app.apis.cars_method import cars_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(cars_blueprint)

