
# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
from datetime import datetime
# import json

from src.db import *
from src.app import create_app
from src.op_exceptions import AttributeRequired
from src.api import system
config = {
    'SQLALCHEMY_DATABASE_URI': ''
}

class TestUser(TestCase):

    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_users(self):
        print "test_get_all_users"

        ###Create Users
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()
        user1 = User(name = "admin user",
                    email = "admin@xyz.com",
                    role=role1)
        user1.save()
        user2 = User(name = "normal user",
                    email="normal@xyz.com",
                    role=role2)
        user2.save()
        r = self.client.get('/users')
        result = json.loads(r.data)
        self.assertEquals(len(result), 2)

    def test_get_one_user(self):
        print "test_get_one_user"

        ### create a User
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()

        user1 = User(name = "admin user",
                    email="admin@xyz.com",
                    role=role1)
        user1.save()
        user2 = User(name="normal user",
                    email="normal@xyz.com",
                    role=role2)
        user2.save()

        r = self.client.get('/users/1')
        result = json.loads(r.data)
        self.assertEqual(result['name'], "admin user")

    def test_update_existing_user(self):
        # Create a user
        # update the same user
        global system
        print "test_update_existing_user"
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()

        user1 = User(name="admin user",
                     email="admin@xyz.com",
                     role=role1)

        user1.save()
        user2 = User(name="normal user",
                     email="normal@xyz.com",
                     role=role2)

        user2.save()

        system.user_set = []
        system.session_set = []

        system.get_users_from_database()
        admin_user = User.get_by_id(1)
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        
        
        #for x in system.session_set:
        #    print x.to_client()

        payload = {'email': 'abcdef@gmail.com',
                   'name': 'NEW ADMIN',
                   'role_id': [1],
                   'session': 'admin@xyz.com'}
        headers = {'content-type': 'application/json'}
        response = self.client.put("/users/2",
                                   data=json.dumps(payload),
                                   headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        print "test_create_new_user"
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()

        user1 = User(name = "admin user",
                     email= "admin@xyz.com",
                     role=role1)

        user1.save()
        user2 = User(name="normal user",
                     email="normal@xyz.com",
                     role=role2)

        user2.save()

        payload = {'email': 'ttt@kkk.com',
                   'name': 'nearly normal user',
                   'role': [2],
                   'session': 't@g.com'}

        headers = {'content-type': 'application/json'}

        response = self.client.post("/users",
                                    data=json.dumps(payload),
                                    headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        global system
        print "test_delete_user"
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()

        user1 = User(name="admin user",
                     email="admin@xyz.com",
                     role=role1)

        user1.save()
        user2 = User(name="normal user",
                     email="normal@xyz.com",
                     role=role2)

        user2.save()
        
        system.session_set = []
        system.user_set = []

        system.get_users_from_database()
        #s=Session(user=user1)
        system.add_session(user1)
        payload = {'session': 'admin@xyz.com'}

        headers = {'content-type': 'application/json'}

        response = self.client.delete("/users/2",
                                      data=json.dumps(payload),
                                      headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_create_role(self):
        print "test_create_role"
        #role1 = Role("admin")
        #role1.save()
        #role2 = Role("user")
        #role2.save()

        #user1 = User(name = "admin user",
        #             email= "admin@xyz.com",
        #             role=role1)

        #user1.save()
        #user2 = User(name="normal user",
        #             email="normal@xyz.com",
        #             role=role2)

        #user2.save()

        payload = {'name': 'owner'}

        headers = {'content-type': 'application/json'}

        response = self.client.post("/roles",
                                    data=json.dumps(payload),
                                    headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_update_role(self):
        # Create a user
        # update the same user
        global system
        print "test_update_role"
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()

        user1 = User(name="admin user",
                     email="admin@xyz.com",
                     role=role1)

        user1.save()
        system.get_users_from_database()
        s=Session(user=user1)
        system.add_session(user1)
        #payload = {'session': 'admin@xyz.com'}
        #user1 = User(name="admin user",
        #             email="admin@xyz.com",
        #             role=role1)

        #user1.save()
        #user2 = User(name="normal user",
        #             email="normal@xyz.com",
        #             role=role2)

        #user2.save()

        #admin_user = User.get_by_id(1)
        #admin_session = Session(user = admin_user)
        #system.session_set.append(admin_session)
        #system.get_users_from_database()
        
        #for x in system.session_set:
        #    print x.to_client()

        payload = {'role': 'owner',
                   'session' : 'admin@xyz.com'
                   }
        headers = {'content-type': 'application/json'}
        response = self.client.put("/roles/2",
                                   data=json.dumps(payload),
                                   headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_delete_role(self):
        global system
        print "test_delete_role"
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()

        user1 = User(name="admin user",
                     email="admin@xyz.com",
                     role=role1)

        user1.save()
        system.get_users_from_database()
        #user2 = User(name="normal user",
        #             email="normal@xyz.com",
        #             role=role2)

        #user2.save()
        
        s=Session(user=user1)
        system.add_session(user1)
        payload = {'session': 'admin@xyz.com'}

        headers = {'content-type': 'application/json'}

        response = self.client.delete("/roles/2",
                                      data=json.dumps(payload),
                                      headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_user_by_email(self):
        print "test_get_user_by_email"

        ###Create Users
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()
        user1 = User(name = "admin user",
                    email = "admin@xyz.com",
                    role=role1)
        user1.save()
        user2 = User(name = "normal user",
                    email="normal@xyz.com",
                    role=role2)
        user2.save()
        
        system.user_set = []
        system.session_set = []

        system.get_users_from_database()

        payload = { 'email' : 'normal@xyz.com' }

        
        headers = {'content-type': 'application/json'}
        response = self.client.get("/users/get_email",
                                   data=json.dumps(payload),
                                   headers=headers)
        result = json.loads(response.data)
        self.assertEquals(result['email'], user2.email)

    def test_get_email_of_user(self):
        print "test_get_email_of_user"

        ###Create Users
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()
        user1 = User(name = "admin user",
                    email = "admin@xyz.com",
                    role=role1)
        user1.save()
        user2 = User(name = "normal user",
                    email="normal@xyz.com",
                    role=role2)
        user2.save()
        
        system.user_set = []
        system.session_set = []

        system.get_users_from_database()
        system.add_session(user1)
        payload = { 'session' : 'admin@xyz.com' }

        
        headers = {'content-type': 'application/json'}
        response = self.client.get("/users/2/email",
                                   data=json.dumps(payload),
                                   headers=headers)
        result = json.loads(response.data)
        self.assertEquals(result['email'], user2.email)

    def test_get_name_of_user(self):
        print "test_get_name_of_user"

        ###Create Users
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()
        user1 = User(name = "admin user",
                    email = "admin@xyz.com",
                    role=role1)
        user1.save()
        user2 = User(name = "normal user",
                    email="normal@xyz.com",
                    role=role2)
        user2.save()
        
        system.user_set = []
        system.session_set = []

        system.get_users_from_database()
        system.add_session(user1)
        payload = { 'session' : 'admin@xyz.com' }

        
        headers = {'content-type': 'application/json'}
        response = self.client.get("/users/2/name",
                                   data=json.dumps(payload),
                                   headers=headers)
        result = json.loads(response.data)
        self.assertEquals(result['name'], user2.name)

    def test_set_email_of_user(self):
        print "test_set_email_of_user"

        ###Create Users
        role1 = Role("admin")
        role1.save()
        role2 = Role("user")
        role2.save()
        user1 = User(name = "admin user",
                    email = "admin@xyz.com",
                    role=role1)
        user1.save()
        user2 = User(name = "normal user",
                    email="normal@xyz.com",
                    role=role2)
        user2.save()
        
        system.user_set = []
        system.session_set = []

        system.get_users_from_database()
        system.add_session(user1)
        payload = { 'session' : 'admin@xyz.com',
                    'email' : 'abcd@xyz.com'
                    }
        
        headers = {'content-type': 'application/json'}
        response = self.client.put("/users/2/email",
                                   data=json.dumps(payload),
                                   headers=headers)
        result = json.loads(response.data)
        self.assertEquals(result['email'], "abcd@xyz.com")

if __name__ == '__main__':
    unittest.main()
