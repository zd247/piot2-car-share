import jwt
import datetime

from app import app, db, bcrypt
from flask_user import UserMixin


class User(db.Model, UserMixin):
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

    # Define the relationship to Role via UserRoles
    # roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.first_name = first_name
        self.last_name = last_name
        self.registered_on = datetime.datetime.now()
    

# ============[Define the Role data-model]===============
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), unique=True)

# # ===============[Define the UserRoles association table]==============
# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# ============[Define black list token for logging out]===============
class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
