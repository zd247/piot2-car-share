import unittest

from app import db
from app.models.car import Car
from tests.base import BaseTestCase

class TestCarModel(BaseTestCase):
    def test_car_init(self):
        car = Car("Honda", "Sedan", "Silver", "White",4, "NYC", 15.5, "12/02/2020")
        self.assertTrue(car is not None)