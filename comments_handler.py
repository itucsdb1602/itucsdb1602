import re
import psycopg2 as dbapi2
import json
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request

from comments_service import CommentService
from comments_class import Comment

comment = Blueprint('comment',__name__)
comment.service = CommentService()

def getHTMLText(pure_html):
    cleanr = re.compile('<.*?>')
    pure_text = re.sub(cleanr, '', pure_html)
    return pure_text

@comment.route('/comments/init')
def init_comment_tbl():
    if request.method == 'GET':
        try:
            comment.service.init_comment_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@comment.route('/comments/add', methods = ['GET', 'POST'])
def add_comment():
    if request.method == "POST":
        if getHTMLText(request.json['comment_text']) == "":
            return jsonify({'status' : 'FAIL', 'errcode' : '00001'})
        commentObject = Comment(request.json['comment_text'], request.json['post_id'])
        try:
            comment.service.add_comment(commentObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@comment.route('/comments/<int:comment_id>', methods = ['GET', 'POST'])
def get_comment(comment_id):
    if request.method == 'GET':
        commentObject = comment.service.get_comment(comment_id)
        return render_template('edit_comment.html',commentObject = commentObject)
    else:
        if getHTMLText(request.json['comment_text']) == "":
            return jsonify({'status' : 'FAIL', 'errcode' : '00001'})
        try:
            comment.service.update_comment(comment_id, request.json['comment_text'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
        return jsonify({'status' : 'OK', 'errcode' : '00000'})




