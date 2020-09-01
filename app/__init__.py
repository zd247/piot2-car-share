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
CORS(app)

# load config setting from env config files
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)


bcrypt = Bcrypt(app) 
jwt = JWTManager(app)

# declare SQLAlchemy 
db = SQLAlchemy(app) 

# declare babel
babel = Babel(app)


# register controller blueprints
from app.views.auth_method import auth_blueprint
from app.views.cars_method import cars_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(cars_blueprint)
    
from app.views import *  