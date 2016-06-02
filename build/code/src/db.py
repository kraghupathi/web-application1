
# -*- coding: utf-8 -*-

from collections import OrderedDict

from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app, request
from sqlalchemy.orm import relationship
import sqlalchemy.types as types

import os
import re
from urlparse import urlparse
from datetime import datetime
import json

from op_exceptions import AttributeRequired, ConstraintError, NotAuthorizedError
from utils import *

db = SQLAlchemy()

#system = None
# Abstract class to hold common methods
class Entity(db.Model):

    __abstract__ = True

    # save a db.Model to the database. commit it.
    def save(self):
        db.session.add(self)
        db.session.commit()

    # update the object, and commit to the database
    def update(self, **kwargs):
        for attr, val in kwargs.iteritems():
            setter_method = "set_" + attr
            try:
                self.__getattribute__(setter_method)(val)
            except Exception as e:
                raise e

        self.save()

    #print "Setting new val"
    #print "Calling %s on %s" % (method_to_set, curr_entity)
    #try:
    #    getattr(record, method_to_set)(new_val)
    #except Exception as e:
    #pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
        if not is_email(value):
            raise TypeError('%s is not an email!' % value)
        self.value = value

    def __str__(self):
        return self.value

class User(Entity):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, **kwargs):
        if 'email' not in kwargs:
            raise AttributeRequired("email is mandatory")

        if 'name' not in kwargs:
            raise AttributeRequired("name is mandatory")

        if 'role' not in kwargs:
            raise AttributeRequired("Atleast one role is mandatory")

        self.set_email(kwargs['email'])
        self.set_name(kwargs['name'])
        self.set_role(kwargs['role'])

    def set_role(self, role):
        self.role = role

    def set_email(self, email):
        if not is_email(email):
            raise TypeError('email is invalid')
        else:
            self.email = email

    def set_name(self, name):
        if not is_alphabetic_string(name):
            raise TypeError('Invalid name')
        else:
            self.name = name

    def set_role(self, role):
        if not isinstance(role, Role):
            raise TypeError('`role` argument should be of type Role.')
        else:
            self.role = role

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role.to_client()
        }

class Role(Entity):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    
    users = db.relationship('User', backref='role')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        return Role.query.all()

    @staticmethod
    def get_by_id(id):
        return Role.query.get(id)

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Session(object):
    user = None
    

    def __init__(self, **kwargs):
        if 'user' not in kwargs:
            raise AttributeRequired("user is mandatory")
        else:
            self._set_user(kwargs['user'])

    def get_user(self):
        return self.user

    def _set_user(self, user):
        if not isinstance(user, User):
            raise TypeError('`user` argument should be of type User.')
        else:
            self.user = user

    def to_client(self):
        return {
            'session': self.user.to_client()
        }

class System(object):

    user_set = []
    session_set = []
    created = False
    

    def __init__(self):
        if System.created == True:
            raise ConstraintError("System has already been created")
        else:
            #a_role = Role("admin")
            #u_role = Role("user")
            #a_role.save()
            #u_role.save()
            #admin_user = User(name="abc", 
            #              email="abc@vlabs.ac.in", 
            #              role=Role.get_by_id(1))
            #admin_user.save()       

            #s = Session(user = admin_user)
            System.created = True
            #self.session_set.append(s)
            #admin_user.save()
            self.session_set = []
            self.user_set = []

    def add_user(self, user,session):
        if session in self.session_set:
            if session.user.role == Role.get_by_id(1):
                user.save()
                self.user_set = User.get_all()
            else:
                raise NotAuthorizedError("Only admin can add")
        else:
            raise ConstraintError("Invalid Session")

#system = None

    def del_user(self, user, session):
        print session.user.email
        if session in self.session_set:
            if not session.user.role.name == "admin":
                raise NotAuthorizedError("Only admin can remove users")
            else:
                check = False
                for x in self.session_set:
                    if x.user.email == user.email:
                        check = True
                if not check:
                    #new_users = filter(lambda x: x.email ==  user.email, self.user_set)
                    user.delete()
                    self.user_set = User.get_all()
                else:
                    raise ConstraintError("User is still logged in")
        else:
            raise ConstraintError("Invalid session!!!")

    def show_users(self,session):
        if session in self.session_set:
            return self.user_set
        else:
            raise ConstraintError("Not a valid session")

    def get_users_from_database(self):
        self.user_set = User.get_all()

    def get_user_by_email(self, email, session):
        user_check = filter(lambda x: x.email == email, self.user_set)
        if session in self.session_set:
            if user_check:
                return user_check[0]
            else:
                raise ConstraintError("Invalid session")
        else:
            raise ConstraintError("No user by this email")

     
    def make_user(self,name,email,role,session):
        if session in self.session_set:
            if(session.user.role==Role.get_by_id(1)):
                user=User(name=name,email=email,role=role)
                self.add_user(user,session)  
            else:
                raise NotAuthorizedError('only admin can create user')
        else:
            raise ConstraintError("Invalid Session")

    def get_email_of_user(self, user, session):
        if session in self.session_set:
            if user in self.user_set:
                return user.email  
            else:
                raise ConstraintError('User does not exist')
        else:
            raise ConstraintError("Invalid Session")

    def get_name_of_user(self, user, session):
        if session in self.session_set:
            if user in self.user_set:
                return user.name  
            else:
                raise ConstraintError('User does not exist')
        else:
            raise ConstraintError("Invalid Session")

    def set_email_of_user(self, user, email, session):
        #global system
        #print self.session_set
        #for x in self.session_set:
        #    print x.user.email
        if session in self.session_set:
            check = filter(lambda x: x.email == email, self.user_set)
            if not check:
                if user in self.user_set:
                    if session.user.role.name == "admin":
                        user.set_email(email)
                        user.update()
                        self.user_set = User.get_all()
                    elif session.user.email == user.email:
                        user.set_email(email)
                        user.update()
                        self.user_set = User.get_all()
                    else:
                        raise NotAuthorizedError("You don't have permission to change the email")
                else:
                    raise ConstraintError('User does not exist')
            else:
                raise ConstraintError("Email already exists")
        else:
            raise ConstraintError("Invalid Session")

    def set_name_of_user(self, user, name, session):
        #global system
        #print self.session_set
        #for x in self.session_set:
        #    print x.user.email
        if session in self.session_set:
            #check = filter(lambda x: x.email == email, self.user_set)
            #if not check:
            if user in self.user_set:
                if session.user.role.name == "admin":
                    user.set_name(name)
                    user.update()
                    self.user_set = User.get_all()
                elif session.user.email == user.email:
                    user.set_name(name)
                    user.update()
                    self.user_set = User.get_all()
                else:
                    raise NotAuthorizedError("You don't have permission to change the name")
            else:
                raise ConstraintError('User does not exist')
        else:
            raise ConstraintError("Invalid Session")

    def get_role_of_user(self, user, session):
        if session in self.session_set:
            if user in self.user_set:
                return user.role  
            else:
                raise ConstraintError('User does not exist')
        else:
            raise ConstraintError("Invalid Session")

    def login(self, user):
        if not user in self.user_set:
            raise ConstraintError("User not in system")
        else:
            self.add_session(user)

    def logout(self, user, session):
        if session in self.session_set:
            if user in self.user_set:
                self.del_session(user, session)
            else:
                raise ConstraintError("user not in system")

        else:
            raise ConstraintError("Invalid session")

    def add_session(self, user):
        check = filter(lambda x: x.email == user.email, self.user_set)
        if check:
            session = Session(user = user)
            self.session_set.append(session)
        else:
            raise ConstraintError("User is not in the system")

    def del_session(self, user, session):
        if session in self.session_set:
            if not user in self.user_set:
                raise ConstraintError("User doesn't exist in system")
            else:
                sessions_list = self.session_set
                new_sessions = filter(lambda x: x.user.email == user.email,
                sessions_list)
                sessions_list = new_sessions
                self.session_set = sessions_list
        else:
            raise ConstraintError("Invalid session")

    def show_sessions(self, session):
        if not session.user.role == Role.get_by_id(1):
            raise NotAuthorizedError("Only admin can view sessions")
        else:
            return self.session_set
