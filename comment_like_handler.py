import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from comment_like_service import CommentLikeService
from comment_like_class import CommentLike

comment_like = Blueprint('comment_like',__name__)
comment_like.service = CommentLikeService()

@comment_like.route('/comment_like/init')
def init_comment_like_tbl():
    if request.method == 'GET':
        try:
            comment_like.service.init_comment_like_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@comment_like.route('/comment_like/add', methods = ['POST'])
def add_comment_like():

    if request.method == 'POST':
        c_like = CommentLike(request.json['user_id'],request.json['comment_id'])
        try:
            comment_like.service.add_comment_like(c_like)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@comment_like.route('/comment_like/delete', methods = ['POST'])
def delete_comment_like():
    if request.method == 'POST':
        c_like = CommentLike(request.json['user_id'],request.json['comment_id'])
        try:
           comment_like.service.delete_comment_like(c_like)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})