import unittest

from app import db
from app.models.user import User, Role
from tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            first_name = 'John',
            last_name = 'Doe'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            first_name = 'John',
            last_name = 'Doe'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

        self.assertTrue(User.decode_auth_token(
            auth_token.decode("utf-8") ) == 1)
        
    def test_init_user_without_role(self):
        # Create 'member@example.com' user with no roles
        if not User.query.filter(User.email == 'member@example.com').first():
            user = User(
                email='member@example.com',
                password="password",
                first_name="Jon",
                last_name="Snow"
            )
            db.session.add(user)
            db.session.commit()
            
        self.assertTrue(user is not None)
        self.assertFalse(user.password == 'password')
        self.assertTrue(user.roles == [])
        
    def test_init_user_with_role(self):
        # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
        if not User.query.filter(User.email == 'member@example.com').first():
            user = User(
                email='member@example.com',
                password="password",
                first_name="Jon",
                last_name="Snow"
            )
            user.roles.append(Role(name='Customer'))
            #TODO: can append more roles but not in this bussiness model not advisable
            
            db.session.add(user)
            db.session.commit()
            
            
        self.assertTrue(user is not None)
        self.assertFalse(user.password == 'password')
        self.assertTrue(user.roles[0].name == 'Customer')
            
        
    def test_black_list_token(self):
        self.assertTrue(True)
        
    def test_check_black_list_token(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
