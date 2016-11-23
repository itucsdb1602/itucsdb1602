import psycopg2 as dbapi2
import json
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
        annoObject = Announcement(request.json['name'],1)# sayi control edilecek!!!!!!
        try:
            announcement.service.add_announcement(annoObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@announcement.route('/announcements', methods = ['GET', 'POST'])
def get_announcements():
    if request.method == 'GET':
        all_announcements = announcement.service.get_all_announcements()
        return render_template('announcements.html',all_announcements = all_announcements)
    else:
        if request.json['op'] == 'delete':
            try:
                announcement.service.delete_announcement(request.json['announcement_id'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

            return jsonify({'status' : 'OK', 'errcode' : '00000'})
        elif request.json['op'] == 'search':
            try:
                announcement_search_result = announcement.service.get_announcements_by_name(request.json['announcement_name'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
            return jsonify({'status' : 'OK', 'errcode' : '00000', 'data' : announcement_search_result})

@announcement.route('/announcements/<int:announcement_id>', methods = ['GET', 'POST'])
def update_announcement(announcement_id):
    if request.method == 'GET':
        upd_announcement = announcement.service.get_announcement(announcement_id)
        return render_template('edit_announcement.html',upd_announcement = upd_announcement);
    else:
        try:
            announcement.service.update_announcement(request.json['id'],request.json['name'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
