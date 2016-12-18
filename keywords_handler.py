import psycopg2 as dbapi2
import json
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from keywords_service import keywordsService
from keywords_class import Keywords
from tag_service import TagService

keywords = Blueprint('keywords',__name__)
keywords.service = keywordsService()

@keywords.route('/keywordss/init')
def init_keywords_tbl():
    if request.method == 'GET':
        try:
            keywords.service.init_keywords_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@keywords.route('/keywordss/add', methods = ['GET', 'POST'])
def add_keywords():
    if request.method == 'GET':
        tagServiceObject = TagService()
        try:
            all_tags = tagServiceObject.get_all_tags()
        except:
            all_tags = None
        return render_template('add_keywords.html',all_tags = all_tags)
    else:
        keywordsObject = Keywords(request.json['name'],request.json['tag_id'])
        try:
            keywords.service.add_keywords(keywordsObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
@keywords.route('/keywordss/get_keywords_by_tag_id', methods = ['GET', 'POST'])
def get_keywordss_by_tag_id():
    if request.method == 'POST':
        try:
                keywords_dropdown_result = keywords.service.get_keywordss_by_tag_id(request.json['tag_id'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
        return jsonify({'status' : 'OK', 'errcode' : '00000', 'data' : keywords_dropdown_result})

@keywords.route('/keywordss', methods = ['GET', 'POST'])
def get_keywordss():
    if request.method == 'GET':
        all_keywordss = keywords.service.get_all_keywordss()
        return render_template('keywordss.html',all_keywordss = all_keywordss)
    else:
        if request.json['op'] == 'delete':
            try:
                keywords.service.delete_keywords(request.json['keywords_id'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

            return jsonify({'status' : 'OK', 'errcode' : '00000'})
        elif request.json['op'] == 'search':
            try:
                keywords_search_result = keywords.service.get_keywordss_by_name(request.json['keywords_name'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
            return jsonify({'status' : 'OK', 'errcode' : '00000', 'data' : keywords_search_result})

@keywords.route('/keywordss/<int:keywords_id>', methods = ['GET', 'POST'])
def update_keywords(keywords_id):
    if request.method == 'GET':
        tagServiceObject = TagService()
        upd_keywords = keywords.service.get_keywords(keywords_id)
        try:
            all_tags = tagServiceObject.get_all_tags()
        except:
            all_tags = None
        return render_template('edit_keywords.html',upd_keywords = upd_keywords,all_tags = all_tags);
    else:
        try:
            keywords.service.update_keywords(request.json['id'],request.json['tag_id'],request.json['name'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
