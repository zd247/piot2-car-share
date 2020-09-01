import json

from flask import request, make_response, jsonify
from app.views.auth_method import UserAPI

def has_role(function):
    """ If this function decorates a controller's action, @login_required is not necessary
        Check for role to access api end point functions
    """
    def wrapper (*args, **kwargs):
        # get current user, if null -> return make_response error
        api = UserAPI().get()
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
            
        print (auth_token)
        # res = self.client.get(
        #         '/auth/status',
        #         headers=dict(
        #             Authorization='Bearer ' + json.loads(
        #                 resp_register.data.decode()
        #         )['auth_token']
        #     )
        # )
        
        # if current_user not null -> check for user role
        
        # if role is satisfied, return the decorated function
        response = function(*args, **kwargs)
        # else return an error response with unauthrorized signal
    
        
        return response

        
        
    return wrapper

# def login_required()
        