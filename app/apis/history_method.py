from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models.history import History

from app.decorator import *

from app import db

history_blueprint = Blueprint('history', __name__, url_prefix="/api/v1/history")

class RestfulAPI (MethodView):
    @jwt_required
    def get(self, event_id = None):
        """ Responds to GET requests """
        try: 
            # expose the list of cars
            if (event_id is None):
                histories = History.query.all()
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
        except Exception as e:
            responseObject = {
                            'status': 'fail',
                            'message': str(e)
                        }
            return make_response(jsonify(responseObject)), 500
        

restful_view = RestfulAPI.as_view('history_api')


# add Rules for API Endpoints
history_blueprint.add_url_rule(
    '',
    view_func=restful_view,
    methods=['POST', 'GET']
)

history_blueprint.add_url_rule(
    '/<string:email>',
    view_func=restful_view,
    methods=['GET', 'PUT', 'DELETE']
)
