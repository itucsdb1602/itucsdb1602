import psycopg2 as dbapi2
import json
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

@tag.route('/tags', methods = ['GET', 'POST'])
def get_tags():
    if request.method == 'GET':
        all_tags = tag.service.get_all_tags()
        return render_template('tags.html',all_tags = all_tags)
    else:
        if request.json['op'] == 'delete':
            try:
                tag.service.delete_tag(request.json['tag_id'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

            return jsonify({'status' : 'OK', 'errcode' : '00000'})
        elif request.json['op'] == 'search':
            try:
                tag_search_result = tag.service.get_tags_by_name(request.json['tag_name'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
            return jsonify({'status' : 'OK', 'errcode' : '00000', 'data' : tag_search_result})

@tag.route('/tags/<int:tag_id>', methods = ['GET', 'POST'])
def update_tag(tag_id):
    if request.method == 'GET':
        upd_tag = tag.service.get_tag(tag_id)
        return render_template('edit_tag.html',upd_tag = upd_tag);
    else:
        try:
            tag.service.update_tag(request.json['id'],request.json['name'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
