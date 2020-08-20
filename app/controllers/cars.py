from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models.car import Car

from app import db

cars_blueprint = Blueprint('cars', __name__, url_prefix="/cars")

def new_car_dict(self, car):
    return {
        'name': car.name,
        'make': car.make,
        'body': car.body,
        'colour': car.colour,
        'seats': car.seats,
        'location': car.location,
        'cost_per_hour': car.cost_per_hour,
        'manu_date': car.manu_date
    }
    
    

class RestfulAPI (MethodView):
    """
    Cars CRUD APIs
    """
    def get(self, car_name = None):
        """ Responds to GET requests """
        # expose the list of cars
        if (car_name is None):
            cars = Car.query.all()
            cars_dict = {}

            for car in cars:
                new_car = new_car_dict(self, car)
                cars_dict[new_car['name']] = new_car
                
            responseObject = {
                        'status': 'success',
                        'message': 'Response to get all cars',
                        'data': cars_dict
                    }
            
            return make_response(jsonify(responseObject)), 200
        else:
            # expose the single car
            car = Car.query.filter_by(name=car_name).first()
            
            new_car = new_car_dict (self, car)
            
            responseObject = {
                        'status': 'success',
                        'message': 'Response to get single car',
                        'data': new_car
                    }
            return make_response(jsonify(responseObject)), 200
        

    def post(self):
        """ Responds to POST requests """
        # get the post body data
        try: 
            post_data = request.get_json()
            
            query_car = Car.query.filter_by(
                name = post_data.get('name')   
            ).first()
            
            if not query_car:
                car = Car (post_data.get('name'),
                           post_data.get('make'),
                           post_data.get('body'),
                           post_data.get('colour'),
                           post_data.get('seats'),
                           post_data.get('location'),
                           post_data.get('cost_per_hour'),
                           post_data.get('manu_date')
                        )
                db.session.add(car)
                db.session.commit()
                
                # parse into dictionary type
                new_car = new_car_dict(self, car)
                               
                responseObject = {
                    'status': 'success',
                    'message': 'New car created',
                    'data': new_car
                }
                
                return make_response(jsonify(responseObject), 201)
                
            else:
                responseObject = {
                    'status': 'Not allowed',
                    'message': 'Car name has already existed'
                }
                return make_response(jsonify(responseObject), 401)
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500
            
            
    def put(self, car_name):
        """ Responds to PUT requests """
        try:
            put_data = request.get_json()
            
            query_car = Car.query.filter_by(
                name = car_name
            ).first()
            
            if query_car:
                query_car.name = put_data.get('name')
                query_car.body = put_data.get('body')
                query_car.make = put_data.get('make')
                query_car.colour = put_data.get('colour')
                query_car.seats = put_data.get('seats')
                query_car.location = put_data.get('location')
                query_car.cost_per_hour = put_data.get('cost_per_hour')
                query_car.manu_date = put_data.get('manu_date')
                
                
                
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500  
            
                
                
        return "Responding to a PUT request"

    def patch(self, entity):
        """ Responds to PATCH requests """
        return "Responding to a PATCH request"

    def delete(self, entity):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"
    
    
    

restful_view = RestfulAPI.as_view('restful_api')

# add Rules for API Endpoints
cars_blueprint.add_url_rule(
    '',
    view_func=restful_view,
    methods=['POST', 'GET']
)

cars_blueprint.add_url_rule(
    '/<string:car_name>',
    view_func=restful_view,
    methods=['GET', 'PUT', 'DELETE']
)