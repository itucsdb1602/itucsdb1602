import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from announcement_service import AnnouncementService
from announcement_class import Announcement

announcement = Blueprint('announcement',__name__)
announcement.service = AnnouncementService()

@announcement.route('/announcements/init')
def init_announcement_tbl():
    if request.method == 'GET':
        try:
            announcement.service.init_announcement_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@announcement.route('/announcements/add', methods = ['GET', 'POST'])
def add_announcement():
    if request.method == 'GET':
        return render_template('add_announcement.html')
    else:
        annoObject = Announcement(request.json['name'],1)
        try:
            announcement.service.add_announcement(annoObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
@announcement.route('/announcements/delete', methods = ['GET', 'POST'])
def delete_announcement():
    if request.method == 'GET':
        return render_template('delete_announcement.html')
    else:
        annoObject = Announcement(request.json['name'],1)
        try:
            announcement.service.delete_announcement(annoObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
@announcement.route('/announcements/getall', methods = ['GET', 'POST'])
def get_announcement():
    if request.method == 'GET':
        return render_template('get_announcement.html')
    else:
        annoObject = Announcement(request.json['name'],1)
        try:
            announcement.service.get_announcement(annoObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
@announcement.route('/announcements/update', methods = ['GET', 'POST'])
def update_announcement():
    if request.method == 'GET':
        return render_template('update_announcement.html')
    else:
        annoObject = Announcement(request.json['name'],1)
        try:
            announcement.service.update_announcement(annoObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})