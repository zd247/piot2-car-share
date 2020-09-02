from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models.user import User

from app import db
from app.decorator import *
from flask_jwt_extended import jwt_required, get_jwt_claims

users_blueprint = Blueprint('users', __name__, url_prefix="/users")

def new_user_dict(self, user):
    return {
        'email': user.email,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role
    }
    

class RestfulAPI (MethodView):
    """
    Users CRUD APIs
    """
    
    @jwt_required
    @has_roles(['admin'])
    def get(self, email = None):
        """ Responds to GET requests """
        try: 
            # expose the list of cars
            if email is None:
                users = User.query.all()
                user_dict = {}

                for user in users:
                    new_user = new_user_dict(self, user)
                    user_dict[new_user['email']] = new_user
                    
                responseObject = {
                            'status': 'success',
                            'message': 'Response to get all users',
                            'data': user_dict
                        }
                
                return make_response(jsonify(responseObject)), 200
            else:
                # expose the single car
                user = User.query.filter_by(email=email).first()
                
                new_user = new_user_dict (self, user)
                
                responseObject = {
                            'status': 'success',
                            'message': 'Response to get single user',
                            'data': new_user
                        }
                return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                            'status': 'fail',
                            'message': str(e)
                        }
            return make_response(jsonify(responseObject)), 500
        

    @jwt_required
    @has_roles(roles=['admin'])
    def post(self):
        """ Responds to POST requests """
        # get the post body data
        try: 
            post_data = request.get_json()
            
            query_user = User.query.filter_by(
                email = post_data.get('email')   
            ).first()
            
            if not query_user:
                user = User (post_data.get('email'),
                           post_data.get('password'),
                           post_data.get('first_name'),
                           post_data.get('last_name'),
                           post_data.get('role')
                        )
                db.session.add(user)
                db.session.commit()
                
                # parse into dictionary type
                new_user = new_user_dict(self, user)
                               
                responseObject = {
                    'status': 'success',
                    'message': 'New user created',
                    'data': new_user
                }
                
                return make_response(jsonify(responseObject), 201)
                
            else:
                responseObject = {
                    'status': 'Not allowed',
                    'message': 'User email has already existed'
                }
                return make_response(jsonify(responseObject), 401)
            
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 500
            
    
    @jwt_required
    @has_roles(['admin'])        
    def put(self, email):
        """ Responds to PUT requests
            Request body must contain all fields    
        """    
        try:
            put_data = request.get_json()
            
            
            # query the car from the params
            query_user = User.query.filter_by(email = email).first()
            

            # modify the queried car with the request body
            if query_user is not None:
                query_user.first_name = put_data.get('first_name')
                query_user.last_name = put_data.get('last_name')
                query_user.role = put_data.get('role')
                
                
                db.session.commit()
                
                updated_user = new_user_dict(self,query_user)
                
                responseObject = {
                    "status": 'success',
                    'message': 'Updated a car successfully',
                    'data': updated_user
                }
                
                return make_response(jsonify(responseObject),200)
                
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Cannot find the user email in query'
                }
                
                return make_response(jsonify(responseObject)), 500
                
            # Car.objects.get(name=car_name).update(**put_data)
        except Exception as e:
            
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject), 500) 
            
    @jwt_required
    @has_roles(['admin'])  
    def delete(self, email):
        """ Responds to DELETE requests """    
        if email:
            try:
                # query the car from the params
                query_user = User.query.filter_by(email = email).first()
                

                # modify the queried car with the request body
                if query_user is not None:
                    db.session.delete(query_user)
                    db.session.commit()
                    
                    responseObject = {
                        'status': 'deleted',
                        'message': 'Successfully deleted a car Record'
                    }
                    
                    return make_response(jsonify(responseObject)), 200
                    
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Cannot find the user email in query'
                    }
                    
                    return make_response(jsonify(responseObject)), 500
                    
                # Car.objects.get(name=car_name).update(**put_data)
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': str(e)
                }
                return make_response(jsonify(responseObject), 500) 


restful_view = RestfulAPI.as_view('restful_api')


# add Rules for API Endpoints
users_blueprint.add_url_rule(
    '',
    view_func=restful_view,
    methods=['POST', 'GET']
)

users_blueprint.add_url_rule(
    '/<string:email>',
    view_func=restful_view,
    methods=['GET', 'PUT', 'DELETE']
)
