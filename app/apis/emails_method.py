from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app.decorator import *
from app import db, mail_server, gmail_account
from app.models.user import User
from app.models.car import Car
from app.apis.cars_method import new_car_dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


emails_blueprint = Blueprint('emails', __name__, url_prefix="/send_email")

class EmailAPI (MethodView):
    @jwt_required
    @has_roles(['admin'])
    def post(self):
        try:
            post_data = request.get_json()
            
            query_user = User.query.filter_by(
                email = post_data.get('engineer_email')
            ).first()
            
            if query_user:
                if query_user.role == 'engineer':
                    
                    query_car = Car.query.filter_by(name = post_data.get('car_name')).first()
                    
                    if query_car:
                        message = MIMEMultipart()
                        message['Subject'] = "The car at this location " + query_car.location + " needs fixing \n"
                        mail_content = "https://www.google.com/maps/search/?api=1&query=" + query_car.location
                        
                        message.attach(MIMEText(mail_content, 'plain'))
                        text = message.as_string()
                
                        mail_server.sendmail(gmail_account, query_user.email, text)
                        
                        reported_car = new_car_dict(self,query_car)
                        
                        responseObject = {
                            'status': 'success',
                            'message': 'Issue reported to engineer',
                            'reported_car': reported_car,
                            'location': query_car.location
                        }
                        return make_response(jsonify(responseObject), 201)
                        
                        
                    else:
                        responseObject = {
                            'status': 'fail',
                            'message': 'No car with name'
                        }
                        return make_response(jsonify(responseObject), 500)
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'User is not an engineer'
                    }
                    return make_response(jsonify(responseObject), 500) 
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'No engineer with email found'
                }
                return make_response(jsonify(responseObject), 500) 
            
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject), 500) 
            
        
email_view = EmailAPI.as_view('email_api')

emails_blueprint.add_url_rule(
    '',
    view_func=email_view,
    methods=['POST']
)