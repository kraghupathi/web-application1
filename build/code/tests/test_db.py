
# -*- coding: utf-8 -*-
import unittest
from flask.ext.testing import TestCase
from datetime import datetime
# import json

from src.db import *
from src.app import create_app
from src.op_exceptions import AttributeRequired, ConstraintError, NotAuthorizedError


config = {
    'SQLALCHEMY_DATABASE_URI': ''
}

system = None

def setUp():
    global system
    a_role = Role("admin")
    u_role = Role("user")
    a_role.save()
    u_role.save()
    admin_user = User(name="admin", 
                          email="app-admin@vlabs.ac.in", 
                          role=Role.get_by_id(1))
    admin_user.save()       
    
    System.created = False
    system = System()
    session = Session(user = admin_user)
    #print " *************SETUP****************"
    #print system
    #print " *************SETUP****************"
    #global system
    #system.login(admin_user)
    system.session_set.append(session)
    system.user_set = User.get_all()
    #print len(system.user_set)


def tearDown():
    global system
    system.user_set = []
    #system.session_set = []

class TestName(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app


    def setUp(self):
        db.create_all()
        setUp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        tearDown()

    def test_name_type(self):
        print "test_name_type"
        new_name = Name("John")
        # correct name
        self.assertEqual(new_name.value, "John")
        # incorrect name
        self.assertRaises(TypeError, Name, "123dasd")

class TestEmail(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        setUp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        tearDown()

    def test_email_type(self):
        print "test_email_type"
        new_email = Email("smith@gmail.com")
        # correct name
        self.assertEqual(new_email.value, "smith@gmail.com")
        # incorrect name
        self.assertRaises(TypeError, Email, "@@@@smithgmail.com")

class TestUser(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        setUp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        tearDown()

    def test_user_creation_without_role(self):
        print "test_user_creation_without_role"
        with self.assertRaises(AttributeRequired):
            user = User(name="Robin Smith", 
                            email="smith@gmail.com")

    def test_user_creation_with_role(self):
        print "test_user_creation_with_role"
        #role = Role("admin")
        #role.save()
        user = User(name="Robin Smith", 
                    email="smith@gmail.com",
                    role=Role.get_by_id(1))
        user.save()
        self.assertEqual(user.role.name, "admin")   

    def test_set_roles_to_user(self):
        print "test_set_roles_to_user"
        #a_role = Role("admin")
        #role.save()
        user = User(name="Robin Smith", 
                    email="smith@gmail.com",
                    role=Role.get_by_id(1))
        user.save()
        #role = Role("user")
        #role.sa
        user.set_role(Role.get_by_id(2))
        user.save()
        users = User.get_all()
        self.assertEqual(users[1].role.name, "user")

    def test_user_get_all(self):
        print "test_user_get_all"
        #role = Role("Admin")
        #role.save()
        user = User(name="Termite", 
                    email="tremite@gmail.com",
                    role=Role.get_by_id(1))
        user.save()
        users = User.get_all()
        self.assertEqual("admin", users[0].role.name)

    def test_get_user_by_id(self):
        print "test_get_user_by_id"
        #role = Role("admin")
        #role.save()
        user = User(name="Robin Smith", 
                    email="smith@gmail.com",
                    role=Role.get_by_id(1))
        user.save()
        self.assertEqual(user.get_by_id(2).role.name, "admin")
        self.assertEqual(user.get_by_id(2).name, "Robin Smith")

    def test_update_user(self):
        print "test_update_role"
        #a_role = Role("admin")
        #a_role.save()
        user = User(name="Robin Smith", 
                    email="smith@gmail.com",
                    role=Role.get_by_id(1))
        user.save()
        u1 = User.get_by_id(1)
        print u1.to_client()
        #u_role = Role("user")
        #u_role.save()
        u1.update(name="Duddley Rod", 
                  email="duddley@gmail.com",
                  role=Role.get_by_id(2))
        print u1.to_client()
        self.assertEqual(u1.get_by_id(1).name, "Duddley Rod")
        self.assertEqual(u1.get_by_id(1).role.name, "user")

class TestRole(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        setUp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        tearDown()
        
    def test_role_creation(self):
        print "test_role_creation"
        role = Role.get_by_id(1)
        role.save()
        self.assertEqual(role.name, "admin")

class TestSession(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        setUp()

    def tearDown(self):
        tearDown()
        

    def test_session_creation(self):
        print "test_session_creation"
        #system = setUp()
        user = User(name="Robin Smith", 
                    email="smith@gmail.com",
                    role=Role.get_by_id(1))
        session = Session(user=user)
        self.assertEqual(session.user.role, Role.get_by_id(1))
        #tearDown(system)

    def test_get_user(self):
        #system = setUp()
        print "test_get_user"
        user = User(name = "def", email = "def@gmail.com", role = Role.get_by_id(1))
        session = Session(user = user)
        new_user = session.get_user()
        self.assertEquals(new_user, user)
        #tearDown(system)

    def test_set_user(self):
        #system = setUp()
        print "test_set_user"
        user = User(name = "def", email = "def@gmail.com", role = Role.get_by_id(2))
        session = Session(user = user)
        session._set_user(user)
        self.assertEquals(session.user, user)
        #tearDown(system)

class TestSystem(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()
        setUp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        tearDown()
    
    def test_system_creation(self):
        print "test_system_creation"
        global system
        #system = System()
        
        #admin_user = User(name="abc", 
        #                  email="abc@vlabs.ac.in", 
        #                  role=Role.get_by_id(1))
        #admin_user.save()
        #print " *************TEST****************"
        #print system
        #print " *************TEST****************"
        new_users = system.user_set
        new_user = new_users[0]
        self.assertEquals(new_user.email, "app-admin@vlabs.ac.in")
        
        

    def test_add_user_session_admin(self):
        global system
        #system = setUp()
        
        print "test_add_user_by_admin"
        old_user_set_length =len( system.user_set)
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        #user.save()
        system.user_set = User.get_all()
        system.add_user(user, admin_session)
        new_user_set_length = len(system.user_set)
        self.assertEquals( new_user_set_length, old_user_set_length + 1)
        #tearDown(system)

    def test_add_user_session_user(self):
        global system
        #system = setUp()
        print "test_add_user_by_user"
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        user1 = User(name = "asdfg", email = "asdf@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #user1.save()
        system.add_user(user1, admin_session)
        system.login(user1)
        user_list = filter(lambda x: x.email == user.email,
        system.user_set)
        user_check = user_list[0]
        user_session = Session(user = user_check)
        system.session_set.append(user_session)
        #global system
        with self.assertRaises(NotAuthorizedError):
            system.add_user(user, user_session)
        #tearDown(system)

    def test_add_user_session_invalid(self):
        global system
        #system = setUp()
        print "test_add_user_session_invalid"
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        user1 = User(name = "asdfg", email = "asdf@gmail.com", role = Role.get_by_id(1))
        #admin_session_list = filter(lambda x: x.user.role == Role.admin, system.session_set)
        #admin_session = admin_session_list[0]
        #system.add_user(user, admin_session)
        #system.login(user)
        #user_session_list = filter(lambda x: x.user.role == Role.user, system.session_set)
        #user_session = user_session_list[0]
        session = Session(user = user1)
        #global system
        with self.assertRaises(ConstraintError):
            system.add_user(user, session)
        #tearDown(system)

    def test_delete_user_session_admin(self):
        global system
        #system = setUp()
        print "test_delete_user_by_admin"
        old_user_set_length =len( system.user_set)
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user, admin_session)
        system.del_user(user, admin_session)
        new_user_set_length = len(system.user_set)
        self.assertEquals( new_user_set_length, old_user_set_length )
        #tearDown(system)

    def test_delete_user_session_user(self):
        global system
        #system = setUp()
        print "test_add_user_by_user"
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        user1 = User(name = "asdfg", email = "asdf@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user1, admin_session)
        system.login(user1)
        system.add_user(user, admin_session)
        user_list = filter(lambda x: x.email == user.email,
        system.user_set)
        user_check = user_list[0]
        user_session = Session(user = user_check)
        system.session_set.append(user_session)
        #global system
        with self.assertRaises(NotAuthorizedError):
            system.del_user(user, user_session)
        #tearDown(system)

    def test_delete_user_session_logged_in(self):
        global system
        #system = setUp()
        print "test_delete_user_session_logged_in"
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        user1 = User(name = "asdfg", email = "asdf@gmail.com", role = Role.get_by_id(1))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        system.login(user)
        #system.add_user(user1, admin_session)
        #user_session_list = filter(lambda x: x.user.role == Role.user, system.session_set)
        #user_session = user_session_list[0]
        #session = Session(user = user1)
        #global system
        with self.assertRaises(ConstraintError):
            system.del_user(user, admin_session)
        #tearDown(system)

    def test_delete_user_session_invalid(self):
        global system
        #system = setUp()
        print "test_delete_user_session_invalid"
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        user1 = User(name = "asdfg", email = "asdf@gmail.com", role = Role.get_by_id(1))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        system.login(user)
        #system.add_user(user1, admin_session)
        #user_session_list = filter(lambda x: x.user.role == Role.user, system.session_set)
        #user_session = user_session_list[0]
        session = Session(user = user1)
        #global system
        with self.assertRaises(ConstraintError):
            system.add_user(user, session)
        #tearDown(system)

    def test_show_users_valid(self):
        print "test_show_users_valid"
        global system
        #system = setUp()
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user,admin_session)
        system.login(user)
        current_session = system.session_set[0]
        
        check_user_set = system.show_users(current_session)
        self.assertEquals(check_user_set, system.user_set)
        #tearDown(system)

    def test_show_users_invalid(self):
        print "test_show_users_invalid"
        global system
        #system = setUp()
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        #admin_sessions_list = filter(lambda x: x.user.role == Role.admin, system.session_set)
        #admin_session = admin_sessions_list[0]
        #system.add_user(user,admin_session)
        #system.login(user)
        current_session = Session(user = user)
        
        with self.assertRaises(ConstraintError):
            system.show_users(current_session)
        #tearDown(system)

    def test_get_user_by_email_existing(self):
        print "test_get_user_by_email_existing"
        #system = setUp()
        global system
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        
        user_check = system.get_user_by_email("abcdef@gmail.com",admin_session)
        self.assertEquals( user_check , user)
        #tearDown(system)
    
    def test_get_user_by_email_non_existent(self):
        print "test_get_user_by_email_non_existent"
        #system = setUp()
        global system
        user = User(name = "ancd", email = "ancd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        system.login(user)
        with self.assertRaises(ConstraintError):
            email_check = system.get_user_by_email("abcbdbejf@gmail.com",admin_session)
        #tearDown(system)

    def test_get_user_by_email_invalid_session(self):
        print "test_get_user_by_email_invalid_session"
        #system = setUp()
        global system
        user = User(name = "abcd", email = "abcd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        session = Session(user = user)
        
        with self.assertRaises(ConstraintError):
            email_check = system.get_user_by_email("abcdf@gmail.com",session)
        #tearDown(system)

    def test_make_user_session_user(self):
        global system
        #system = setUp()
        print "test_make_user_session_user"
        old_users=system.user_set
        user = User(name = "abcd", email = "abcd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user,admin_session)
        system.login(user)
        user_list = filter(lambda x: x.email == user.email,
        system.user_set)
        user_check = user_list[0]
        user_session = Session(user = user_check)
        system.session_set.append(user_session)
        with self.assertRaises(NotAuthorizedError):
            system.make_user("abc", "abcd@gmail.com", user.role, user_session)
        #tearDown(system)

    def test_make_user_session_admin(self):
        global system
        #system = setUp()
        print "test_make_user_session_admin"
        #old_users=system.user_set
        #user = User(name = "abcd", email = "abcd@gmail.com", role = Role.user)
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #session = Session(user = user)
        old_user_set_length = len(system.user_set)
        system.make_user("abc", "abcd@gmail.com", admin_session.user.role, admin_session)
        new_user_set_length = len(system.user_set)
        self.assertEquals(old_user_set_length + 1, new_user_set_length)
        #tearDown(system)

    def test_make_user_session_invalid_session(self):
        global system
        #system = setUp()
        print "test_make_user_session_admin"
        old_users=system.user_set
        user = User(name = "abcd", email = "abcd@gmail.com", role = Role.get_by_id(2))
        #admin_session_list = filter(lambda x: not x.user.role == Role.admin, system.session_set)
        #admin_session = admin_session_list.pop()
        session = Session(user = user)
        with self.assertRaises(ConstraintError):
            system.make_user("abc", "abcd@gmail.com", Role.get_by_id(1), session)
        #tearDown(system)

    def test_get_email_of_user_valid(self):
        #system = setUp()
        global system
        print "test_get_email_of_user_valid"
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user, admin_session)
        system.login(user)
        
        user_check = system.get_email_of_user(user, admin_session)
        self.assertEquals( user_check , user.email)
        #tearDown(system)
    
    def test_get_email_of_user_invalid_user(self):
        #system = setUp()
        global system
        print "test_get_email_of_user_invalid_user"
        user = User(name = "ancd", email = "ancd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #system.add_user(user, admin_session)
        #system.login(user)
        with self.assertRaises(ConstraintError):
            email_check = system.get_email_of_user(user ,admin_session)
        #tearDown(system)
    
    def test_get_email_of_user_invalid_session(self):
        print "test_get_email_of_user_invalid_session"
        #system = setUp()
        global system
        user = User(name = "abcd", email = "abcd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        session = Session(user = user)
        
        with self.assertRaises(ConstraintError):
            email_check = system.get_email_of_user(user ,session)
        #tearDown(system)

    def test_get_name_of_user_valid(self):
        print "test_get_name_of_user_valid"
        #system = setUp()
        global system
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user, admin_session)
        system.login(user)
        
        user_check = system.get_name_of_user(user, admin_session)
        self.assertEquals( user_check , user.name)
        #tearDown(system)
    
    def test_get_name_of_user_invalid_user(self):
        print "test_get_name_of_user_invalid_user"
        #system = setUp()
        global system
        user = User(name = "ancd", email = "ancd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #system.add_user(user, admin_session)
        #system.login(user)
        with self.assertRaises(ConstraintError):
            email_check = system.get_name_of_user(user ,admin_session)
        #tearDown(system)
    
    def test_get_name_of_user_invalid_session(self):
        print "test_get_name_of_user_invalid_session"
        #system = setUp()
        global system
        user = User(name = "abcd", email = "abcd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        session = Session(user = user)
        
        with self.assertRaises(ConstraintError):
            email_check = system.get_name_of_user(user ,session)
        #tearDown(system)
        

    def test_set_email_of_user_valid_admin(self):
       
        print "test_set_email_of_user_valid_admin"
        global system
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #system.login(admin_user)
        system.add_user(user, admin_session)
        system.login(user)
        #user_session = Session(user = user)
        #system.session_set.append(user_session)
        system.set_email_of_user(user, "abcdef123@gmail.com", admin_session)
        user_check = system.get_email_of_user(user, admin_session)
        self.assertEquals( user_check , user.email)
    
    def test_set_email_of_user_valid_user(self):
        global system
        #system = setUp()
        print "test_set_name_of_user_valid_user"
        user = User(name = "ancd", email = "ancd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        system.login(user)
        user_list = filter(lambda x: x.email == user.email,
        system.user_set)
        user_check = user_list[0]
        user_session = Session(user = user_check)
        system.session_set.append(user_session)
        system.set_email_of_user(user, "abcdefghi@gmail.com", user_session)
        user_check = system.get_email_of_user(user, admin_session)
        self.assertEquals(user_check, user.email)
        #tearDown(system)       
    
    def test_set_email_of_user_invalid_session(self):
        print "test_set_email_of_user_invalid_session"
        #system = setUp()
        global system
        user = User(name = "abcd", email = "abcd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        session = Session(user = user)
        
        with self.assertRaises(ConstraintError):
            email_check = system.set_email_of_user(user, "abcdef@gmail.com", session)
        #tearDown(system)
    

    def test_set_email_of_user_invalid_email(self):
        print "test_set_name_of_user_invalid_email"
        #system = setUp()
        global system
        user = User(name = "abcd", email = "abcd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        session = Session(user = user)
        
        with self.assertRaises(ConstraintError):
            email_check = system.set_email_of_user(user, "abcd@gmail.com", admin_session)
        #tearDown(system)
        

    def test_get_role_of_user_valid(self):
        print "test_get_role_of_user_valid"
        #system = setUp()
        global system
        user = User(name = "abcdef", email = "abcdef@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user, admin_session)
        system.login(user)
        
        user_check = system.get_role_of_user(user, admin_session)
        self.assertEquals( user_check , user.role)
        #tearDown(system)
    
    def test_get_role_of_user_invalid_user(self):
        print "test_get_role_of_user_invalid_user"
        #system = setUp()
        global system
        user = User(name = "ancd", email = "ancd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #system.add_user(user, admin_session)
        #system.login(user)
        with self.assertRaises(ConstraintError):
            email_check = system.get_role_of_user(user ,admin_session)
        #tearDown(system)
    
    def test_get_role_of_user_invalid_session(self):
        print "test_get_role_of_user_invalid_session"
        #system = setUp()
        global system
        user = User(name = "abcd", email = "abcd@gmail.com", role = Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        session = Session(user = user)
        
        with self.assertRaises(ConstraintError):
            email_check = system.get_role_of_user(user ,session)
        #tearDown(system)       

    def test_login_valid(self):
        print "test_login_valid"
        global system
        #system = setUp()
        user = User(name = "abcdefghi", email = "abcdefghi@gmail.com", role =
        Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        old_session_set_length = len(system.session_set)
        system.login(user)
        new_session_set_length = len(system.session_set)
        self.assertEquals(old_session_set_length + 1, new_session_set_length)
        #tearDown(system)

    def test_login_invalid(self):
        print "test_login_invalid"
        global system
        #system = setUp()
        user = User(name = "abcdef", email = "abcdef@gmail.com", role =
        Role.get_by_id(2))
        with self.assertRaises(ConstraintError):
            system.login(user)
        #tearDown(system)

    def test_logout_valid(self):
        print "test_logout_valid"
        global system
        #system = setUp()
        user = User(name = "abcdefghi", email = "abcdefghi@gmail.com", role =
        Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        old_session_set_length = len(system.session_set)
        system.login(user)
        user_list = filter(lambda x: x.email == user.email,
        system.user_set)
        user_check = user_list[0]
        user_session = Session(user = user_check)
        system.session_set.append(user_session)
        system.logout(user, user_session)
        new_session_set_length = len(system.session_set)
        self.assertEquals(old_session_set_length , new_session_set_length)
        #tearDown(system)

    def test_logout_invalid_user(self):
        print "test_logout_invalid_user"
        global system
        #system = setUp()
        user = User(name = "abcdefghi", email = "abcdefghi@gmail.com", role =
        Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #system.add_user(user, admin_session)
        #old_session_set_length = len(system.session_set)
        #system.login(user)
        #user_session_list = filter(lambda x: x.user.email == user.email,
        #system.session_set)
        #user_session = user_session_list[0]
        #system.logout(user, user_session)
        #new_session_set_length = len(system.session_set)
        #self.assertEquals(old_session_set_length , new_session_set_length)
        with self.assertRaises(ConstraintError):
            system.logout(user, admin_session)
        #tearDown(system)

    def test_logout_invalid_session(self):
        print "test_logout_invalid_session"
        global system
        #system = setUp()
        user = User(name = "abcdefghi", email = "abcdefghi@gmail.com", role =
        Role.get_by_id(2))
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        system.add_user(user, admin_session)
        #old_session_set_length = len(system.session_set)
        system.login(user)
        #user_session_list = filter(lambda x: x.user.email == user.email,
        #system.session_set)
        #user_session = user_session_list[0]
        #system.logout(user, user_session)
        #new_session_set_length = len(system.session_set)
        #self.assertEquals(old_session_set_length , new_session_set_length)
        session = Session(user = user)
        with self.assertRaises(ConstraintError):
            system.logout(user, session)
        #tearDown(system)

    def test_add_session(self):
        print "test_add_session"
        #system = setUp()
        global system
        user = User(name = "ghtfdh", email = "ghtfdh@gmail.com", role = Role.get_by_id(2))
        #ession = Session(user = user)
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user,admin_session)
        old_session_set_length = len(system.session_set)
        system.add_session(user)
        new_session_set_length = len(system.session_set)
        self.assertEquals(new_session_set_length, old_session_set_length + 1)
        #tearDown(system)

    def test_del_session_valid(self):
        print "test_delete_session_valid"
        #system = setUp()
        global system
        user = User(name = "ghtfdh", email = "ghtfdh@gmail.com", role = Role.get_by_id(2))
        session = Session(user = user)
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user,admin_session)
        system.login(user)
        old_session_set_length = len(system.session_set)
        system.add_session(user)
        system.del_session(user,admin_session)
        new_session_set_length = len(system.session_set)
        self.assertEquals(new_session_set_length, old_session_set_length-1)
        #tearDown(system)

    def test_del_session_invalid_user(self):
        print "test_delete_session_invalid_user"
        #system = setUp()
        global system
        user = User(name = "asddghj", email = "asljfbd@gmail.com", role = Role.get_by_id(2))
        session = Session(user = user)
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        #system.add_user(user,admin_session)
        #old_session_set_length = len(system.session_set)
        #system.add_session(user)
        #system.del_session(user)
        #new_session_set_length = len(system.session_set)
        #self.assertEquals(new_session_set_length, old_session_set_length)
        with self.assertRaises(ConstraintError):
            system.del_session(user, admin_session)
        #tearDown(system)

    def test_del_session_invalid_session(self):
        print "test_delete_session_invalid_session"
        #system = setUp()
        global system
        user = User(name = "asddghj", email = "asljfbd@gmail.com", role = Role.get_by_id(2))
        session = Session(user = user)
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user,admin_session)
        #old_session_set_length = len(system.session_set)
        #system.add_session(user)
        session = Session(user = user)
        #system.del_session(user)
        #new_session_set_length = len(system.session_set)
        #self.assertEquals(new_session_set_length, old_session_set_length)
        with self.assertRaises(ConstraintError):
            system.del_session(user, session)
        #tearDown(system)
    

    def test_show_sessions_admin(self):
        print "test_show_sessions_admin"
        global system
        #system = setUp()
        #check_user_set = system.user_set
        #self.assertEquals(check_user_set, system.show_users())
        user = User(name = "ghtfdh", email = "ghtfdh@gmail.com", role = Role.get_by_id(2))
        session = Session(user = user)
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user,admin_session)
        system.add_session(user)
        check_session_set= system.show_sessions(admin_session)
        self.assertEquals(check_session_set, system.session_set)
        #tearDown(system)

    def test_show_sessions_user(self):
        print "test_show_sessions_user"
        global system
        #system = setUp()
        #check_user_set = system.user_set
        #self.assertEquals(check_user_set, system.show_users())
        user = User(name = "ghtfdh", email = "ghtfdh@gmail.com", role = Role.get_by_id(2))
        session = Session(user = user)
        admin_users = filter(lambda x: x.role == Role.get_by_id(1), system.user_set)
        admin_user = admin_users[0]
        admin_session = Session(user = admin_user)
        system.session_set.append(admin_session)
        #global system
        system.add_user(user,admin_session)
        system.add_session(user)
        with self.assertRaises(NotAuthorizedError):
            check = system.show_sessions(session)
        #tearDown(system)

if __name__ == '__main__':
    unittest.main()
