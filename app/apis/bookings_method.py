
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models.car import Car

from app.decorator import *

from app import db, gcalendar_service

bookings_blueprint = Blueprint('bookings', __name__, url_prefix="/bookings/<string:car_name>")

class BookingAPI (MethodView):
    @jwt_required
    @has_roles(['admin', 'customer'])  
    def get(self, car_name, event_id = None):
        """ View all events of the params car's calendar id """
        try: 
            # find car by name
            query_car = Car.query.filter_by(name = car_name).first()
            
            if query_car is not None:
                # get car calendar id
                calendar_id = query_car.calendar_id
                
                if (event_id is None):                    
                    # return all events with respective car's calendar id
                    event  = gcalendar_service.events().get(calendarId = calendar_id).execute()
                    page_token = None
                    while True:
                        events = gcalendar_service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
                        
                        page_token = events.get('nextPageToken')
                        if not page_token:
                            break
                        
                        responseObject = {
                            'status': 'success',
                            'message': events['items']
                        }
                    
                        return make_response(jsonify(responseObject),200)
                else:
                    event  = gcalendar_service.events().get(calendarId = calendar_id, eventId = event_id).execute()
                    
                    responseObject = {
                        'status': 'success',
                        'message': event
                    }
                    
                    return make_response(jsonify(responseObject),200)
                    
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Cannot find the car name in query'
                }
                        
                return make_response(jsonify(responseObject)), 500
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 500

            
    @jwt_required
    @has_roles(['customer'])  
    def post(self, car_name):
        """ As a current user, create an event from the car's calendar id """
        try: 
            post_data = request.get_json()
            
            current_user = get_jwt_identity()
            
            # find car by name
            query_car = Car.query.filter_by(name = car_name).first()
            
            if query_car is not None:

                event = {
                    'summary': current_user['email'],
                    'location': query_car.location,
                    'description': current_user['email'] + ' booking for ' + car_name,
                    'start': {
                        'dateTime': post_data.get('start_time'), #'2020-09-09T06:39:56.000Z'
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': post_data.get('end_time'),
                        'timeZone': 'America/Los_Angeles',
                    },
                    'attendees': [
                        {'email': current_user['email']},
                    ],
                    
                }

                created_event = gcalendar_service.events().insert(
                    calendarId=query_car.calendar_id,
                    body=event,
                    maxAttendees = 1,
                    sendNotifications = True,
                    sendUpdates ='none',
                ).execute()
                
                responseObject = {
                        'status': 'created',
                        'event': created_event
                    }
                                
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Cannot find the car name in query'
                }
                            
                return make_response(jsonify(responseObject)), 500
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 500
          
    
    def put (self, car_name, event_id):
        """ As a current user, create an event from the car's calendar id """ 
        try:
            put_data = request.get_json()
                
            current_user = get_jwt_identity()
                
            # find car by name
            query_car = Car.query.filter_by(name = car_name).first()
                
            if query_car is not None:
                # First retrieve the event from the API.
                event = gcalendar_service.events().get(calendarId=query_car.calendar_id, eventId=event_id).execute()

                event['summary'] = put_data.get('summary')
                event['location'] = put_data.get('location')
                event['description'] = put_data.get('description')
                event['start'] = put_data.get('start')
                event['end'] = put_data.get('end')
                event['attendees'] = put_data.get('attendees')

                updated_event = gcalendar_service.events().update(calendarId=query_car.calendar_id,
                                                                eventId=event['id'],
                                                                body=event).execute()

                # Print the updated date.
                responseObject = {
                        'status': 'updated',
                        'updated_event': updated_event
                    }
                                        
                return make_response(jsonify(responseObject)), 202

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            
            return make_response(jsonify(responseObject)), 500
        
        
        
    @jwt_required
    @has_roles(['admin', 'customer'])  
    def delete(self, car_name, event_id):
        """ Cancel car booking as user """
        try:
            query_car = Car.query.filter_by(name = car_name).first()
            if (query_car is not None):
                # call the delete api from google calendar
                gcalendar_service.events().delete(calendarId=query_car.calendar_id, eventId=event_id).execute()

                responseObject = {
                    'status': 'deleted',
                    'message': 'Successfully canceled a booking'
                }
                return make_response(jsonify(responseObject)), 202
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Cannot find the car name in query'
                }
                return make_response(jsonify(responseObject)), 500    
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': str(e)
            }
            return make_response(jsonify(responseObject)), 500
        

        
booking_view = BookingAPI.as_view('booking_api')


bookings_blueprint.add_url_rule(
    '/<string:event_id>',
    view_func=booking_view,
    methods=['GET', 'PUT', 'DELETE']
)

bookings_blueprint.add_url_rule(
    '/',
    view_func=booking_view,
    methods=['GET', 'POST'],
)