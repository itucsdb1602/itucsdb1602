import psycopg2 as dbapi2
import json
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from keywords_service import keywordsService
from keywords_class import keywords

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
        return render_template('add_keywords.html')
    else:
        keywordsObject = keywords(request.json['name'])
        try:
            keywords.service.add_keywords(keywordsObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
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
        upd_keywords = keywords.service.get_keywords(keywords_id)
        return render_template('edit_keywords.html',upd_keywords = upd_keywords);
    else:
        try:
            keywords.service.update_keywords(request.json['id'],request.json['name'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
