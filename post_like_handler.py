import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from post_like_service import PostLikeService
from post_like_class import PostLike

pLikes = Blueprint('pLikes',__name__)
pLikes.service = PostLikeService()

@pLikes.route('/pLikes/init')
def init_pLikes_tbl():
    if request.method == 'GET':
        try:
            pLikes.service.init_post_like_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@pLikes.route('/pLikes/add', methods = ['GET', 'POST'])
def add_pLikes():

    if request.method == 'POST':
        pL = PostLike(request.json['user_id'],request.json['post_id'])
        try:
            pLikes.service.add_post_like(pL)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@pLikes.route('/pLikes/delete', methods = ['GET', 'POST'])
def delete_pLike():
    if request.method == 'POST':
        pL = PostLike(request.json['user_id'],request.json['post_id'])
        try:
           pLikes.service.delete_post_like(pL)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})