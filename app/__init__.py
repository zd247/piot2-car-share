import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# init app and cors
app = Flask(__name__, instance_relative_config=True)
CORS(app)

# load config setting from env
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# declare bcrypt to hash password
bcrypt = Bcrypt(app) 

# declare SQLAlchemy 
db = SQLAlchemy(app) 

from app.controllers.auth import auth_blueprint
from app.controllers.cars import cars_blueprint

# register controller blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(cars_blueprint)
