import psycopg2 as dbapi2
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