
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app.decorator import *

from app import db

bookings_blueprint = Blueprint('bookings', __name__, url_prefix="/bookings")

class BookingAPI (MethodView):
    @jwt_required
    @has_roles(['admin', 'customer'])  
    def get(self):
        """ View car rental history (booking history) """
    
    @jwt_required
    @has_roles(['customer'])  
    def post(self):
        """ Book a car as an user """
        # TODO: talk to google calendar
        
    @jwt_required
    @has_roles(['admin', 'customer'])  
    def delete(self):
        """ Cancel car booking as user """
        #TODO: talk with google calendar and update database
        
booking_view = BookingAPI.as_view('booking_api')

bookings_blueprint.add_url_rule(
    '',
    view_func=booking_view,
    methods=['POST']
)