import unittest

from app import db, gcalendar_service
from app.models.car import Car
from tests.base import BaseTestCase

class TestCarModel(BaseTestCase):
    def test_car_init(self):
        car = Car("Honda_Test", "Sedan", "Silver", "White",4, "NYC", 15.5, "12/02/2020")
        self.assertTrue(car is not None)
        self.assertTrue(car.calendar_id is not None)
        
        # clean up
        gcalendar_service.calendars().delete(calendarId=car.calendar_id).execute()