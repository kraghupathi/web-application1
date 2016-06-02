
# -*- coding: utf-8 -*-

import os
import csv
import requests
from datetime import datetime
import inspect
from flask import session, render_template, Blueprint, request, jsonify, abort, current_app, redirect, url_for
from config import *
from flask import current_app

from flask import Flask, redirect, url_for
from werkzeug import secure_filename

from db import *
from utils_new import parse_request, jsonify_list
api = Blueprint('APIs', __name__)

system = System()

@api.route('/users', methods=['GET'])
def get_users():
    global system
    system.get_users_from_database()
    return jsonify_list([i.to_client() for i in system.user_set])

@api.route('/roles', methods=['GET'])
def get_roles():
    return jsonify_list([i.to_client() for i in Role.get_all()])

@api.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    record = User.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("user", id))

    return jsonify(record.to_client())

@api.route('/roles/<int:id>', methods=['GET'])
def get_role_by_id(id):
    record = Role.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("role", id))

    return jsonify(record.to_client())

# not implemented for session, implement with session
@api.route('/users', methods=['POST'])
def create_user():

    ### Check if there is a session and act according to the specification
    global system
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400)
    else:
        name = request.json['name']
        email = request.json['email']
        role = request.json['role']
        session_email = request.json['session']

        try:
            user = User(name=name,
                        email=email,
                        role=Role.get_by_id(role))

            user.save()
            system.user_set = User.get_all()
            return jsonify(user.to_client())
        except Exception, e:
            current_app.logger.error("Error occured while inserting"
                                     "user record: %s" % str(e))
            abort(500, str(e))

@api.route('/roles', methods=['POST'])
def create_role():
    if not request.json or not 'name' in request.json:
        abort(400)
    else:
        name = request.json['name']
        try:
            role = Role(name)
            role.save()
            return jsonify(role.to_client())
        except Exception, e:
            current_app.logger.error("Error occured while inserting" 
                                     "role record: %s" % str(e))
            abort(500, str(e))

@api.route('/users/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_user(id):
    global system
    session = None
    ### Check if there is a session and act according to the specification
    #if 'session' not in request.json:
    #    print "throw error"
    #else:
    #    print "Check according to your specification"
    

    
    #print request.json['session']

    #admin_user = User.get_by_id(1)
    #system.add_session(admin_user)
    #session = system.session_set[0]
                   
    system.get_users_from_database()
    record = User.get_by_id(id)
    if not record:
        abort(404, 'No %s with id %s' % (user, id))

    if request.method == 'DELETE':
    
        delete_session_email= request.headers.get('session')
        delete_session = None
        for x in system.session_set:
            if x.user.email == delete_session_email:
                delete_session = x
        try:
            #record.delete()
            system.del_user(record,delete_session)
            return jsonify(id=id, status="success")
        except Exception, e:
            current_app.logger.error("Error occured while deleting"
                                     "user record %d: %s" % (id, str(e)))
            abort(500, str(e))

    if request.method == 'PUT':
    
        print system.session_set
        for x in system.session_set:
            print x.user.email
        for s in system.session_set:
            if s.user.email==request.json['session']:
                session=s
    
        print session.user.email
        new_data = {}
        try:
            if 'name' in request.json:
                #new_data['name'] = request.json['name']
                system.set_name_of_user(record, request.json['name'], session)
            if 'email' in request.json:
                #new_data['email'] = request.json['email']
                system.set_email_of_user(record, request.json['email'], session)
            if 'role_id' in request.json:
                role = Role.get_by_id(request.json['role_id'])
                #new_data['role'] = role

            record.role = role
            record.update()

            return jsonify(User.get_by_id(id).to_client())

        except Exception, e:
            current_app.logger.error("Error occured while updating"
                                     " user record %d: %s" % (id, str(e)))
            abort(500, str(e))

@api.route('/roles/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_role(id):

    if 'session' not in request.json:
        abort(400)
    else:
        print "choose according to configuraton"
    record = Role.get_by_id(id)
    if not record:
        abort(404, 'No %s with id %s' % (role, id))

    if request.method == 'DELETE':
        try:
            record.delete()
            return jsonify(id=id, status="success")
        except Exception, e:
            current_app.logger.error("Error occured while deleting "
                                     "role record %d: %s" % (id, str(e)))
            abort(500, str(e))

    if request.method == 'PUT':
        try:
            if 'role' in request.json:
                record.role = request.json['role']

            record.update()
            
            return jsonify(Role.get_by_id(id).to_client())

        except Exception, e:
            current_app.logger.error("Error occured while updating "
                                     "role record %d: %s" % (id, str(e)))
            abort(500, str(e))

@api.route('/users/get_email', methods=['GET'])
def get_user_by_email():
    global system
    system.get_users_from_database()

    if 'email' not in request.json:
        abort(400)
    else:
        print "choose according to configuraton"
    
    record = None

    for x in system.user_set:
        if x.email == request.json['email']:
            record = x
    
    if not record:
        abort(404, "No entry for %s with id: %s found." % ("user", id))

    return jsonify(record.to_client())

@api.route('/users/<int:id>/email', methods=['GET'])
def get_email_of_user(id):
    global system

    session = None
    system.get_users_from_database()
    if 'session' not in request.json:
        abort(400)
    else:
        print "choose according to configuraton"
    

    for s in system.session_set:
        if s.user.email==request.json['session']:
            session=s
    record = User.get_by_id(id)         
    if not record:
        abort(404, 'No %s with id %s' % (user, id))

        

    #if email_check == "email":
    #system.user_set = User.get_all()
    #record = User.get_by_id(id)
    new_data = {}
    new_data['email'] = system.get_email_of_user(record, session)        
    #if not record:
    #    abort(404, "No entry for %s with id: %s found." % ("user", id))

    return jsonify(new_data)

@api.route('/users/<int:id>/name', methods=['GET'])
def get_name_of_user(id):
    global system

    session = None
    system.get_users_from_database()
    if 'session' not in request.json:
        abort(400)
    else:
        print "choose according to configuraton"
    

    for s in system.session_set:
        if s.user.email==request.json['session']:
            session=s
    record = User.get_by_id(id)         
    if not record:
        abort(404, 'No %s with id %s' % (user, id))

        

    #if email_check == "email":
    #system.user_set = User.get_all()
    #record = User.get_by_id(id)
    new_data = {}
    new_data['name'] = system.get_name_of_user(record, session)        
    #if not record:
    #    abort(404, "No entry for %s with id: %s found." % ("user", id))

    return jsonify(new_data)

@api.route('/users/<int:id>/email', methods=['PUT'])
def change_user_email(id):

    record = User.get_by_id(id)
    global system

    system.get_users_from_database()
    if not record:
        abort(404, 'No %s with id %s' % (user, id))

    session = None
    #system.get_users_from_database()
    if 'session' not in request.json:
        abort(400)
    else:
        print "choose according to configuraton"
    

    for s in system.session_set:
        if s.user.email==request.json['session']:
            session=s
    

#    if request.method == 'DELETE':
#        try:
#            record.delete()
#            return jsonify(id=id, status="success")
#        except Exception, e:
#            current_app.logger.error("Error occured while deleting"
#                                     "user record %d: %s" % (id, str(e)))
#            abort(500, str(e))

#    if request.method == 'PUT':
    #if email_update == "change_email":
    new_data = {}
    try:
            #if 'name' in request.json:
        new_data['name'] = system.get_name_of_user(record, session)
        if 'email' in request.json:
            new_data['email'] = request.json['email']
            #if 'roles' in request.json:
            #    role_ids = request.json['roles']
            #    roles = []
            #    for role_id in role_ids:
            #        roles.append(Role.get_by_id(role_id))
        new_data['role'] = system.get_role_of_user(record,session)
        #new_data['session'] = record.session
        record.update(**new_data)
        system.get_users_from_database()
        return jsonify(User.get_by_id(id).to_client())

    except Exception, e:
        current_app.logger.error("Error occured while updating"
                                     "user record %d: %s" % (id, str(e)))
        abort(500, str(e))

@api.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        if ('email' in session):
            return render_template("user-list.html")
        else:
            return render_template("login.html")

@api.route("/auth/login", methods=['GET', 'POST'])
def login():
    global system
    user=None
    if request.method == 'POST':
        email = str(request.form['email'])
        url_for_getting_the_user = "%s/users" % \
                                   (APP_URL)
        backend_resp = requests.get(url_for_getting_the_user)
        user_list = backend_resp.json()
        if len(backend_resp.text.encode('ascii')) != 2:
            count = 0
            for user in range(len(user_list)):
                print len(user_list)
                print user_list[user]
                if str(email) == str(user_list[user]['email']):
                    current_app.logger.info("Successfully Logged in")
                    session['email'] = str(user_list[user]['email'])
                    session['role_name'] = str(user_list[user]['role']['name'])
                    session['user_id'] = str(user_list[user]['id'])
                    for u in system.user_set:
                        if u.email==str(email):
                           user=u
                    system.login(user)
                    print system.session_set
                    for x in system.session_set:
                        print x.user.email
                    return redirect("/")
                else:
                    count = count + 1
            if count == len(user_list):
                return render_template("login.html", message="Invalid email id")
            
@api.route('/auth/logout', methods=['GET'])
def logout_handler():
    global system
    
    
    user=None
    ses=None
    for s in system.session_set:
        if(s.user.email == session['email'] ):
            ses=s
    for u in system.user_set:
        if(u.email == session['email']):
            user=u
    system.logout(user,ses)
    session.pop('email', None)
    session.pop('role_name', None)   
    return redirect("/")
