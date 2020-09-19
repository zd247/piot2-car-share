from flask import request, make_response, jsonify
from functools import wraps
from app import jwt
from flask_jwt_extended import get_jwt_claims

def has_roles(roles):
    def decorator(function):
        @wraps(function)
        def wrapper (*args, **kwargs):
            # get current user, if null -> return make_response error
            current_user_role = get_jwt_claims()['role']
            
            if current_user_role not in roles:
                responseObject = {
                    'status': 'fail',
                    'message': 'Not authorized'
                }
                return make_response(jsonify(responseObject)), 401
                
            
            # if current_user not null -> check for user role
            
            # if role is satisfied, return the decorated function
            response = function(*args, **kwargs)
            # else return an error response with unauthrorized signal
        
            
            return response

        return wrapper
    
    return decorator
        