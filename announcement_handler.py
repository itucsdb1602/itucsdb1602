import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from announcement_service import AnnouncementService
from announcement_class import Announcement
from crypt import methods

announcement = Blueprint('announcement',__name__)
announcement.service = AnnouncementService()

@announcement.route('/announcements/init')
def init_tag_database():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE announcements (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            fromuserid INT NOT NULL,
            crt_time TIMESTAMP NOT NULL
        )"""
        cursor.execute(query)
        connection.commit()

@announcement.route('/announcements/add', methods = ['GET', 'POST'])
def add_announcement():
    if request.method == 'GET':
        return render_template('add_announcement.html')
    else:
        annoObject = Announcement(request.json['name'],1)
        announcement.service.add_announcement(annoObject)
        return jsonify({'status':'OK'});