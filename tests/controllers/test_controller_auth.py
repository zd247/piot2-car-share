import time
import json
import unittest

from app import db
from app.models.user import User
from tests.base import BaseTestCase


def register_user(self, email, password, first_name, last_name, role=None) :
    return self.client.post(
        '/api/v1/auth/register',
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
        '/api/v1/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )

def logout_user(self, auth_token):
    return self.client.post(
        '/api/v1/auth/logout',
        headers=dict(
            Authorization='Bearer ' + auth_token
        )
    )
    

class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration without roles"""
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456', "John", "Doe")
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            
            self.assertTrue(data['role'] == 'customer')
            
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
    
    def test_registration_with_roles(self):
        """ Test for user registration with roles"""
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456', "John", "Doe", role='manager')
            data = json.loads(response.data.decode())
            
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            
            self.assertTrue(data['role'] == 'manager')
            
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = User(
            email='joe@gmail.com',
            password='test',
            first_name = 'Doe',
            last_name='John',
            role="customer"
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe")
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 500)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe")
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

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        """ Test for user status """
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe", role='engineer')
            response = self.client.get(
                '/api/v1/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            
            self.assertTrue(data['data']['role'] == 'engineer')
            
            self.assertTrue(data['data']['email'] == 'joe@gmail.com')
            self.assertEqual(response.status_code, 200)

    def test_user_status_malformed_bearer_token(self):
        """ Test for user status with malformed bearer token"""
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456', "Joe", "Doe")
            response = self.client.get(
                '/api/v1/auth/status',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
