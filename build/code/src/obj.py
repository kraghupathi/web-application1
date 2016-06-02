
# -*- coding: utf-8 -*-
from op_exceptions import AttributeRequired
from utils import *

class Name(object):
    value = None
    def __init__(self, value):
        # value: String 
        # if the string contains any non-alphabet and non-space character,
        # raise a type error
        if is_alphabetic_string(value):
            self.value = value
        else:
            raise TypeError('%s is not a Name!' % value)

    def __str__(self):
        return self.value

class Email(object):
    value = None
    def __init__(self, value):
        if is_email(value):
            self.value = value
        else:
            raise TypeError('%s is not a Email!' % value)
    def __str__(self):
        return self.value
        

class Role(object):
    name = None
    admin = None
    user = None

    def __init__(self, name):
        self.name = name

Role.admin = Role("admin")
Role.user = Role("user")

class User(object):
    name = None
    email = None
    role = None

    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            raise AttributeRequired("mandatory attribute `name` is missing")
        self.set_name(kwargs['name'])

        if 'email' not in kwargs:
            raise AttributeRequired("mandatory attribute `email` is missing")
        self.set_email(kwargs['email'])

        if 'role' not in kwargs:
            raise AttributeRequired("mandatory attribute `role` is missing")
        self.set_role(kwargs['role'])

    def set_email(self, email):
        self.email = email.value

    def set_name(self, name):
        self.name = name.value

    def set_role(self, role):
        self.role = role.name

    def get_role(self):
        return self.role

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

#    @staticmethod
#    def get_all():
#        return users

    def to_client(self):
        return {
            'name': self.name,
            'email': self.email,
            'role': self.role.to_client()
        }

class Session(object):
    user = None

    def __init__(self, **kwargs):
        if 'user' not in kwargs:
            raise AttributeRequired('mandatory variable `user` is missing!')
        self._set_user_session(kwargs['user'])

    def _set_user_session(self, user):
        if not isinstance(user, User):
            raise TypeError('`user` argument should be of type user')
        else:
            self.user = user

    def get_user_session(self):
        return self.user

class System():
    user_set = []
    session_set = []
    already_initialized = False

    def __init__(self):
        if not System.already_initialized:
            admin_user = User(name=Name('admin'), email=Email('admin@vlabs.ac.in'), role=Role.admin)
            System.user_set.append(admin_user)
            System.already_initialized = True
        else:
            raise ConstraintError('System is already initialized!')

    def make_user(self, name, email, role):
        if not isinstance(name, Name):
            raise ConstraintError('`name` should be of type Name')
        if not isinstance(email, Email):
            raise ConstraintError('`email` should be of type Email')
        if not isinstance(role, Role):
            raise ConstraintError('`role` should be of type Role')
        user = User(name=name, email=email, role=role)
        return user

    def add_user(self, user):
        if not isinstance(user, User):
            raise TypeError('user should be of type `User`') 
        if user in System.user_set:
            return
        else:
            duplicate = False
            for element in System.user_set:
                if element.email == user.email:
                    duplicate = True
                    break
            if not duplicate:
                System.user_set.append(user)
        return

    def del_user(self, user):
        if not isinstance(user, User):
            raise TypeError('user should be of type `User`') 
        if user not in System.user_set:
            return
        System.user_set.remove(user)
        del user

    def show_users(self):
        return System.user_set

    def get_user_by_email(self, email):
        if not isinstance(email, Email):
            raise TypeError('email should be of type `Email`') 
        for element in System.user_set:
            if element.email == email.value:
                return element

    def login(self, user):
        if not isinstance(user, User):
            raise TypeError('user should be of type `User`')
        registered = False
        for element in System.user_set:
            if element.email == user.email:
                registered = True
        if registered:
            for element in System.session_set:
                 if element.email == user.email:
                     return
            System.session_set.append(user)
        return

    def del_session(self, user):
        System.session_set.remove(user)
        return

    def show_sessions(self):
        return System.session_set
