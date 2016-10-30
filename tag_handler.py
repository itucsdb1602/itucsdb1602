import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from tag_service import TagService
from tag_class import Tag

tag = Blueprint('tag',__name__)
tag.service = TagService()

@tag.route('/tags/init')
def init_tag_tbl():
    if request.method == 'GET':
        try:
            tag.service.init_tag_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@tag.route('/tags/add', methods = ['GET', 'POST'])
def add_tag():
    if request.method == 'GET':
        return render_template('add_tag.html')
    else:
        tagObject = Tag(request.json['name'])
        try:
            tag.service.add_tag(tagObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})