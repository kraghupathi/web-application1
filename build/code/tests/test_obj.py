
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from datetime import datetime

from src.obj import *
from src.op_exceptions import AttributeRequired

class TestName(TestCase):
    TESTING = True
    def test_name_type(self):
        print "test_name_type"
        new_name = Name("raghu")
        # correct name
        self.assertEqual(new_name.value, "raghu")
        # incorrect name
        self.assertRaises(TypeError, Name, "123dasd")

class TestEmail(TestCase):
    TESTING = True
    def test_email_type(self):
        print "test_email_type"
        new_email = Email("raghu@vlabs.ac.in")
        # correct email
        self.assertEqual(new_email.value, "raghu@vlabs.ac.in")
        # incorrect email
        self.assertRaises(TypeError, Email, "123")

class TestRole(TestCase):
    TESTING = True
    def test_role_admin(self):
        print "test_role_admin"
        self.assertEqual(Role.admin.name, 'admin')
    
    def test_role_user(self):
        print "test_role_user"
        self.assertEqual(Role.user.name, "user")

class TestUser(TestCase):
    TESTING = True

    def test_user_creation(self):
        print "test_user_creation"
        user = User(name=Name('raghu'), email=Email('raghupathi@vlabs.ac.in'), role=Role.admin)
        self.assertEqual(isinstance(user, User), True)
        self.assertEqual(user.name, 'raghu')
        self.assertEqual(user.email, 'raghupathi@vlabs.ac.in')
        self.assertEqual(user.role, 'admin')

    def test_user_set_email(self):
        print "test_user_set_email"
        user = User(name=Name('raghu'), email=Email('raghupathi@vlabs.ac.in'), role=Role.admin)
        new_email = Email('newemail@vlabs.ac.in')
        user.set_email(new_email)
        self.assertEqual(user.email, new_email.value)

    def test_user_set_name(self):
        print "test_user_set_name"
        user = User(name=Name('raghu'), email=Email('raghupathi@vlabs.ac.in'), role=Role.admin)
        new_name = Name('newname')
        user.set_name(new_name)
        self.assertEqual(user.name, new_name.value)

    def test_user_set_role(self):
        print "test_user_set_role"
        user = User(name=Name('raghu'), email=Email('raghupathi@vlabs.ac.in'), role=Role.admin)
        new_role = Role.user
        user.set_role(new_role)
        self.assertEqual(user.role, new_role.name)

    def test_user_get_role(self):
        print "test_user_get_role"
        user = User(name=Name('raghu'), email=Email('raghu@vlabs.ac.in'), role=Role.admin)
        self.assertEqual(user.get_role(), 'admin')

    def test_user_get_email(self):
        print "test_user_get_email"
        user = User(name=Name('raghu'), email=Email('raghupathi@vlabs.ac.in'), role=Role.admin)
        self.assertEqual(user.get_email(), 'raghupathi@vlabs.ac.in')

    def test_user_get_name(self):
        print "test_user_get_name"
        user = User(name=Name('raghu'), email=Email('raghu@vlabs.ac.in'), role=Role.admin)
        self.assertEqual(user.get_name(), 'raghu')

    def test_user_get_all(self):
        print "test_user_get_all"

class TestSession(TestCase):
    TESTING = True

    def test_session_creation(self):
        print "test_session_creation"
        user = User(name=Name('raghu'), email=Email('raghupathi@vlabs.ac.in'), role=Role.admin)
        session = Session(user=user)
        self.assertEqual(isinstance(session, Session), True)
        self.assertEqual(session.user, user)

    def test_set_user_session(self):
        print "test_set_user_session"
        user = User(name=Name('raghu'), email=Email('raghupathi@vlabs.ac.in'), role=Role.admin)
        session = Session(user=user)
        new_user = User(name=Name('newuser'), email=Email('newuser@vlabs.ac.in'), role=Role.user)
        session._set_user_session(new_user)
        self.assertEqual(session.user, new_user)

    def test_get_user_session(self):
        print "test_get_user_session"
        user = User(name=Name('user'), email=Email('user@vlabs.ac.in'), role=Role.user)
        session = Session(user=user)
        self.assertEqual(session.get_user_session(), user)

class TestSystem(TestCase):
    TESTING = True

    def setUp(self):
        pass

    def tearDown(self):
        if len(system.user_set) > 1:
            del system.user_set[-1]
        system.already_initialized = False

    def test_system_constructor(self):
        print "test_system_constructor"
        user = system.user_set[0]
        self.assertEqual(isinstance(user, User), True)
        self.assertEqual(user.name, 'admin')
        self.assertEqual(user.email, 'admin@vlabs.ac.in')
        self.assertEqual(user.role, 'admin')

    def test_make_user(self):
        print "test_make_user"
        name = Name('yogesh')
        email = Email('yogesh@vlabs.ac.in')
        role = Role.admin
        user = system.make_user(name=name, email=email, role=role)
        self.assertEqual(isinstance(user, User), True)
        self.assertEqual(user.name, name.value)

    def test_add_user(self):
        print "test_add_user"
        user = User(name=Name('a'), email=Email('a@a.com'), role=Role.user)
        system.add_user(user)
        userFromSystem = system.user_set[-1]
        self.assertEqual(userFromSystem, user)

    def test_del_user(self):
        print "test_del_user"
        user = User(name=Name('a'), email=Email('a@a.com'), role=Role.admin)
        system.user_set.append(user)
        system.del_user(user)
        is_present = True
        if user not in system.user_set:
            is_present = False
        self.assertEqual(is_present, False)   

    def test_show_users(self):
        print "test_show_users"
        user = User(name=Name('a'), email=Email('a@a.com'), role=Role.admin)
        system.user_set.append(user)
        userList = system.show_users()
        present = False
        if user in userList:
            present = True
        self.assertEqual(present, True)

    def test_get_user_by_email(self):
        print "test_get_user_by_email"
        user = User(name=Name('a'), email=Email('a@a.com'), role=Role.admin)
        email = Email('a@a.com')
        system.user_set.append(user)
        returnedUser = system.get_user_by_email(email)
        self.assertEqual(user, returnedUser)
        system.user_set.remove(user)
        del user

    def test_login(self):
        print "test_login"
        user = User(name=Name('a'), email=Email('a@a.com'), role=Role.admin)
        system.user_set.append(user)
        system.login(user)
        logedin = False
        if user in system.session_set:
            logedin = True
        self.assertEqual(logedin, True)

    def test_del_session(self):
        print "test_del_session"
        user = system.user_set[0]
        system.session_set.append(user)
        system.del_session(user)
        deleted = False
        if user not in system.session_set:
            deleted = True
        self.assertEqual(deleted, True)

    def test_show_sessions(self):
        print "test_show_sessions"
        user = User(name=Name('a'), email=Email('a@a.com'), role=Role.admin)
        system.user_set.append(user)
        system.session_set.append(user)
        sessionList = system.show_sessions()
        present = False
        if user in sessionList:
            present = True
        self.assertEqual(present, True)

if __name__ == '__main__':
    system = System()
    unittest.main()
