import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from group_user_service import GroupUserService
from group_user_class import GroupUser

gUsers = Blueprint('gUsers',__name__)
gUsers.service = GroupUserService()

@gUsers.route('/gUsers/init')
def init_gUsers_tbl():
    if request.method == 'GET':
        try:
            gUsers.service.init_group_user_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@gUsers.route('/gUsers/add', methods = ['GET', 'POST'])
def add_gUsers():

    if request.method == 'POST':
        gU = GroupUser(request.json['user_id'],request.json['group_id'],1)
        try:
            gUsers.service.add_group_user(gU)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@gUsers.route('/gUsers/delete', methods = ['GET', 'POST'])
def delete_gUsers():
    if request.method == 'POST':
        gU = GroupUser(request.json['user_id'],request.json['group_id'])
        try:
           gUsers.service.delete_group_user(gU)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})