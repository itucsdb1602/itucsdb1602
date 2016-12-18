import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from post_keywords_service import PostKeywrodsService
from post_keywords_class import PostKeywords
from keywords_class import Keywords

pKeywordss = Blueprint('pKeywordss',__name__)
pKeywordss.service = PostKeywrodsService()

@pKeywordss.route('/pKeywordss/init')
def init_pKeywordss_tbl():
    if request.method == 'GET':
        try:
            pKeywordss.service.init_post_keywords_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@pKeywordss.route('/pKeywordss/add', methods = ['GET', 'POST'])
def add_pKeywordss():

    if request.method == 'POST':
        pL = PostKeywords(request.json['keywords_id'],request.json['post_id'])
        try:
            pKeywordss.service.add_post_keywords(pL)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@pKeywordss.route('/pKeywordss/get', methods = ['GET', 'POST'])

def get_pKeywordss():
    if request.method == 'POST':
        try:
            all_keywords_related_post = pKeywordss.service.get_all_post_keywords(request.json['post_id'])
        except dbapi2.Error as e:
            all_keywords_related_post = None

        return jsonify({'status' : 'OK', 'errcode' : '00000', 'data' : all_keywords_related_post})

@pKeywordss.route('/pKeywordss/delete', methods = ['GET', 'POST'])
def delete_pKeywords():
    if request.method == 'POST':
        pL = PostKeywords(request.json['keywords_id'],request.json['post_id'])
        try:
           pKeywordss.service.delete_post_keywords(pL)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})