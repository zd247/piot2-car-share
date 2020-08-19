import time
import json
import unittest

from app import db
from app.models.car import Car
from tests.base import BaseTestCase

#TODO: write test for each response return from the controller

def seed_car(self):
    car1 = Car("Honda", "Sedan", "Silver", "White",4, "NYC", 15.5, "2018-12-19 09:26:03.478039")
    self.assertTrue(car1 is not None)
    car2 = Car("Subaru", "Truck", "Yellow", "White",7, "BC", 23.5, "2018-12-20 09:26:03.478039")
    self.assertTrue(car2 is not None)
    db.session.add_all([car1, car2])
    db.session.commit()

class TestCarBlueprint(BaseTestCase):
    def test_get_all(self):
        """ Test get all cars """
        # add dummy cars
        seed_car(self)
        
        with self.client:
            response = self.client.get('/cars', content_type='application/json')
            data = json.loads(response.data.decode())
            
            self.assertEqual(data['data']['Subaru']['make'],'Truck')
            self.assertTrue(len(data['data']) == 2)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data is not None)
                
    def test_get_one(self):
        """ Test get a single car by primary key """
        seed_car(self)
        
        with self.client:
            response = self.client.get('/cars/Subaru', content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertTrue(data is not None)
            self.assertEqual(data['data']['make'],'Truck')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
    
    def test_create_new(self):
        """ Test create a new a car via POST """
        
        with self.client:
            response = self.client.post(
                '/cars',
                data=json.dumps(dict(
                    name='Test',
                    make='Test',
                    body='Test',
                    colour='Test',
                    seats=4,
                    location='Test',
                    cost_per_hour=17.5,
                    manu_date='2018-12-19 09:26:03.478039',
                )),
                content_type='application/json',
            )
            
            data  = json.loads(response.data.decode())
            print (data)
            self.assertTrue(data is not None)
            self.assertEqual(data['data']['name'], 'Test')
            self.assertEqual(data['data']['make'], 'Test')
            self.assertEqual(data['data']['seats'], 4)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            
            
            
            
            