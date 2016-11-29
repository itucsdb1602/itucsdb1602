import psycopg2 as dbapi2
import json
from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask.globals import current_app, request
from post_service import PostService
from post_class import Post
from tag_service import TagService

post = Blueprint('post',__name__)
post.service = PostService()

@post.route('/posts/init')
def init_post_tbl():
    if request.method == 'GET':
        try:
            post.service.init_post_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
@post.route('/posts/add', methods = ['GET', 'POST'])
def add_post():
    if request.method == 'GET':
        tagServiceObject = TagService()
        all_tags = tagServiceObject.get_all_tags()
        return render_template('add_post.html',all_tags = all_tags)
    else:
        postObject = Post(request.json['post_text'], request.json['tag_id'], request.json['title'])
        try:
            post.service.add_post(postObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@post.route('/posts/<int:post_id>', methods = ['GET', 'POST'])
def get_post(post_id):
    if request.method == 'GET':
        postObject = post.service.get_post(post_id)
        return render_template('post.html',postObject = postObject)
    else:
        try:
            post.service.delete_post(post_id)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@post.route('/posts_edit/<int:post_id>', methods = ['GET', 'POST'])
def update_post(post_id):
    if request.method == 'GET':
        tagServiceObject = TagService()
        all_tags = tagServiceObject.get_all_tags()
        postObject = post.service.get_post(post_id)
        return render_template('edit_post.html', postObject = postObject, all_tags = all_tags)
    else:
        try:
            post.service.update_post(post_id,request.json['title'],request.json['tag_id'],request.json['post_text'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

