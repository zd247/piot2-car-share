import jwt
import datetime

from app import app, db, bcrypt
from flask_user import UserMixin
from flask_jwt_extended import get_jwt_claims

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"
    
    email = db.Column(db.String(255), nullable=False, unique=True, primary_key=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    registered_on = db.Column(db.DateTime, nullable=False)
    
    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # roles = db.relationship('Role', secondary='user_roles')
    role  = db.Column(db.String(30), nullable=False, server_default='customer')

    def __init__(self, email, password, first_name, last_name, role):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.registered_on = datetime.datetime.now()