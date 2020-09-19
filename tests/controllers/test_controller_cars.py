import time
import json
import unittest

from app import db, gcalendar_service
from app.models.car import Car
from tests.base import BaseTestCase

#TODO: write test for each response return from the controller

def seed_car(self):
    car1 = Car("Honda1", "Sedan", "Silver", "White",4, "NYC", 15.5, "2018-12-19 09:26:03.478039")
    self.assertTrue(car1 is not None)
    car2 = Car("Subaru1", "Truck", "Yellow", "White",7, "BC", 23.5, "2018-12-20 09:26:03.478039")
    self.assertTrue(car2 is not None)
    db.session.add_all([car1, car2])
    db.session.commit()
    return car1.calendar_id, car2.calendar_id

def register_user(self, email, password, first_name, last_name, role=None) :
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role = role
        )),
        content_type='application/json',
    )

def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )   

class TestCarBlueprint(BaseTestCase):
    def test_get_all(self):
        """ Test get all cars """
        # add dummy cars
        cal_id1, cal_id2 = seed_car(self)
        
        with self.client:
            # admin register
            resp_register = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe", "admin")
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # admin login
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            
            # api calls 
            response = self.client.get('/cars',
                    content_type='application/json',
                    headers=dict(
                    Authorization='Bearer ' + data['auth_token']
                ))
            data = json.loads(response.data.decode())
            
            self.assertEqual(data['data']['Subaru1']['make'],'Truck')
            self.assertTrue(len(data['data']) == 2)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data is not None)
            self.assertTrue(data['data']['Honda1']['calendar_id'] is not None)
            self.assertTrue(data['data']['Subaru1']['calendar_id'] is not None)
            
            gcalendar_service.calendars().delete(calendarId=cal_id1).execute()
            gcalendar_service.calendars().delete(calendarId=cal_id2).execute()
                
    def test_get_one(self):
        """ Test get a single car by primary key """
        cal_id1, cal_id2 = seed_car(self)
        
        with self.client:
            # admin register
            resp_register = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe", "admin")
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            
            # admin login
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            
            # perform api call
            response = self.client.get('/cars/Subaru1',
                    content_type='application/json',
                    headers=dict(
                    Authorization='Bearer ' + data['auth_token']
                ))
            data = json.loads(response.data.decode())
            self.assertTrue(data is not None)
            self.assertEqual(data['data']['make'],'Truck')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            
            self.assertTrue(data['data']['calendar_id'] is not None)
                    
            gcalendar_service.calendars().delete(calendarId=cal_id1).execute()
            gcalendar_service.calendars().delete(calendarId=cal_id2).execute()
    
    def test_create_new(self):
        """ Test create a new a car via POST """
        
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe", "admin")
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            
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
                headers=dict(
                    Authorization='Bearer ' + data['auth_token']
                )
            )
            
            data  = json.loads(response.data.decode())
            
            self.assertTrue(data is not None)
            self.assertEqual(data['data']['name'], 'Test')
            self.assertEqual(data['data']['make'], 'Test')
            self.assertEqual(data['data']['seats'], 4)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            gcalendar_service.calendars().delete(calendarId=data['data']['calendar_id']).execute()
            
    def test_edit_existing (self):
        """ Test put method on existing database unit """
        cal_id1, cal_id2 = seed_car(self)
        
        assert_car1 = db.session.query(Car).filter_by(name='Honda1').first()
        assert_car2 = db.session.query(Car).filter_by(name='Subaru1').first()
        
        self.assertTrue(assert_car1 is not None)
        self.assertTrue(assert_car2 is not None)
        
        
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe", "admin")
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            # invoke put request to client with new body being passed
            response = self.client.put (
                '/cars/Honda1',
                data = json.dumps(dict(
                    name='Honda1',
                    make='Test',
                    body='Test',
                    colour='Test',
                    seats=7,
                    location='Test',
                    cost_per_hour=12.5,
                    manu_date='2018-12-19 09:26:03.478039',
                )),
                content_type = 'application/json',
                headers=dict(
                    Authorization='Bearer ' + data['auth_token']
                )
                
            )
        
            data = json.loads(response.data.decode())
            
            # test the response object and status
            self.assertTrue(data is not None)
            self.assertEqual(data['data']['name'], 'Honda1')
            self.assertEqual(data['data']['make'], 'Test')
            self.assertEqual(data['data']['seats'], 7)
            self.assertEqual(data['data']['cost_per_hour'], 12.5)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            
            gcalendar_service.calendars().delete(calendarId=cal_id1).execute()
            gcalendar_service.calendars().delete(calendarId=cal_id2).execute()
            
            
    def test_delete_existing(self):
        """ Test delete method on an existing Car record """
        
        cal_id1, cal_id2 = seed_car(self)
        
        assert_car1 = db.session.query(Car).filter_by(name='Honda1').first()
        assert_car2 = db.session.query(Car).filter_by(name='Subaru1').first()
        
        self.assertTrue(assert_car1 is not None)
        self.assertTrue(assert_car2 is not None)
        
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe", "admin")
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            
            response = self.client.delete(
                '/cars/Honda1',
                headers=dict(
                    Authorization='Bearer ' + data['auth_token']
                )
            )
            
            query_car = db.session.query(Car).filter_by(name='Honda1').first()
            
        
            self.assertFalse(query_car)
            self.assertEqual(response.status_code, 200)
            
            gcalendar_service.calendars().delete(calendarId=cal_id1).execute()
            gcalendar_service.calendars().delete(calendarId=cal_id2).execute()
        
            
            