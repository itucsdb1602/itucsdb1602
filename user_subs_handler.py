import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from user_subs_service import UserSubsService
from user_subs_class import UserSubs

uSubs = Blueprint('uSubs',__name__)
uSubs.service = UserSubsService()

@uSubs.route('/uSubs/init')
def init_uSubs_tbl():
    if request.method == 'GET':
        try:
            uSubs.service.init_user_subs_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@uSubs.route('/uSubs/add', methods = ['GET', 'POST'])
def add_uSubs():

    if request.method == 'POST':
        pL = UserSubs(request.json['user_id'],request.json['tag_id'])
        try:
            uSubs.service.add_user_subs(pL)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@uSubs.route('/uSubs/delete', methods = ['GET', 'POST'])
def delete_pLike():
    if request.method == 'POST':
        pL = UserSubs(request.json['user_id'],request.json['tag_id'])
        try:
           uSubs.service.delete_user_subs(pL)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})