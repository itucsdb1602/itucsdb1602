import psycopg2 as dbapi2
import json
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from group_service import GroupService
from group_class import Group

group = Blueprint('group',__name__)
group.service = GroupService()

@group.route('/groups/init')
def init_group_tbl():
    if request.method == 'GET':
        try:
            group.service.init_group_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@group.route('/groups/add', methods = ['GET', 'POST'])
def add_group():
    if request.method == 'GET':
        return render_template('add_group.html')
    else:
        groupObject = Group(request.json['name'])
        try:
            group.service.add_group(groupObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@group.route('/groups', methods = ['GET', 'POST'])
def get_groups():
    if request.method == 'GET':
        all_groups = group.service.get_all_groups()
        return render_template('groups.html',all_groups = all_groups)
    else:
        if request.json['op'] == 'delete':
            try:
                group.service.delete_group(request.json['group_id'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

            return jsonify({'status' : 'OK', 'errcode' : '00000'})
        elif request.json['op'] == 'search':
            try:
                group_search_result = group.service.get_group_by_name(request.json['group_name'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
            return jsonify({'status' : 'OK', 'errcode' : '00000', 'data' : group_search_result})

@group.route('/groups/<int:group_id>', methods = ['GET', 'POST'])
def update_group(group_id):
    if request.method == 'GET':
        upd_group = group.service.get_group(group_id)
        return render_template('edit_group.html',upd_group = upd_group);
    else:
        try:
            group.service.update_group(request.json['id'],request.json['name'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
