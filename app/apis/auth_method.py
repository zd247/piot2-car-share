import numpy as np
import json

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app import bcrypt, db, blacklist
from app.models.user import User

from app.decorator import *

from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity,
                                set_access_cookies, set_refresh_cookies,
                                get_jwt_claims, get_raw_jwt)


auth_blueprint = Blueprint('auth', __name__, url_prefix="/api/v1/auth")

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        
        # create new user if ok
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    first_name = post_data.get('first_name'),
                    last_name = post_data.get('last_name'),
                    role= post_data.get('role')
                )
                
                    
                # insert the user to database
                db.session.add(user)
                db.session.commit()
                
    
                # generate the auth token
                access_token = create_access_token(identity=post_data)
                refresh_token = create_refresh_token(identity=post_data)
                
                
                # roles = json.dumps(user.roles, cls=AlchemyEncoder) #TODO: when have more than 5 roles
                
                # construct res message
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': access_token,
                    'role': user.role
                }
                
                response = make_response(jsonify(responseObject))
                
                
                response.set_cookie('role',user.role)
                response.set_cookie('access_token',access_token, max_age=86400)
                response.set_cookie('email', str(user.email))
                response.set_cookie('first_name', str(user.first_name))
                response.set_cookie('last_name', str(user.last_name))
                
                return response, 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': str(e)
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 500

class LoginAPI(MethodView):
    """
    User Login Resource
    """
    def post(self):
        # get the post body data
        post_data = request.get_json()
        
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            
            if user and bcrypt.check_password_hash(user.password, post_data.get('password')):
                # construct indentity data
                post_data['first_name'] = user.first_name
                post_data['last_name'] = user.last_name
                post_data['registered_on'] = user.registered_on
                post_data['role'] = user.role

                
                access_token = create_access_token(identity=post_data)
                refresh_token = create_refresh_token(identity=post_data)
                
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': access_token,
                    'role': user.role
                }
                response = make_response(jsonify(responseObject))
                
                
                response.set_cookie('role',user.role)
                response.set_cookie('access_token',access_token, max_age=86400)
                response.set_cookie('email', str(user.email))
                response.set_cookie('first_name', str(user.first_name))
                response.set_cookie('last_name', str(user.last_name))
                
                return response, 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 500


class UserAPI(MethodView):
    """
    User Resource
    """
    @jwt_required
    def get(self):
        # get the auth token
        try:
            current_user = get_jwt_identity()
            
            responseObject = {
                'status': 'success',
                'data': {
                    'email': current_user['email'],
                    'first_name': current_user['first_name'],
                    'last_name': current_user['last_name'],
                    'role': current_user['role']
                }
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 500
       
class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    @jwt_required
    def delete(self):    
        try:
            jti = get_raw_jwt()['jti']
            blacklist.add(jti)
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 200
        
class RefreshAPI(MethodView):
    """ 
        Refresh accessing token resource
    """
    
    @jwt_refresh_token_required
    def post (self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        
        resp = jsonify({'refresh': True})
        ret = {
            'auth_token': access_token
        }
        set_access_cookies(resp, access_token)
        return jsonify(ret), 200
        
    

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')
refresh_view = RefreshAPI.as_view('refresh_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/logout',
    view_func=logout_view,
    methods=['DELETE']
)
auth_blueprint.add_url_rule(
    '/refresh',
    view_func=refresh_view,
    methods=['POST']
)


# ========================[External]=======================

# from sqlalchemy.ext.declarative import DeclarativeMeta

# class AlchemyEncoder(json.JSONEncoder):
    
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     json.dumps(data) # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             # a json-encodable dict
#             return fields

#         return json.JSONEncoder.default(self, obj)
