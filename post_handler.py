import psycopg2 as dbapi2
import json
import re
from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask.globals import current_app, request
from post_service import PostService
from post_class import Post
from tag_service import TagService
from comments_service import CommentService

post = Blueprint('post',__name__)
post.service = PostService()

def getHTMLText(pure_html):
    cleanr = re.compile('<.*?>')
    pure_text = re.sub(cleanr, '', pure_html)
    return pure_text

@post.route('/posts/init')
def init_post_tbl():
    if request.method == 'GET':
        try:
            post.service.init_post_tbl()
        except dbapi2.Error as e:
            return jsonify({
                'status' : 'FAIL',
                'errcode' : e.pgcode,
                'errmsg' : e.diag.message_primary
                })

        return jsonify({
            'status' : 'OK',
            'errcode' : '00000'
            })
@post.route('/posts/add', methods = ['GET', 'POST'])
def add_post():
    if request.method == 'GET':
        tagServiceObject = TagService()
        all_tags = tagServiceObject.get_all_tags()
        return render_template('add_post.html',all_tags = all_tags)
    else:
        errList = [];
        if getHTMLText(request.json['post_text']) == "":
            errList.append("Post Content cannot be empty!")
        if request.json['tag_id'] == "":
            errList.append("Tag must be assigned!")
        if request.json['title'] == "":
            errList.append("Title cannot be empty!")
        if len(errList) != 0:
            return jsonify({
                'status' : 'FAIL',
                'errmsg': errList
                })

        postObject = Post(request.json['post_text'], request.json['tag_id'], request.json['title'])
        try:
            lastRowID = post.service.add_post(postObject)
        except dbapi2.Error as e:
            if e.diag.message_primary.find("title") > 0 & e.diag.message_primary.find("unique"):
                errList.append("Title is used. Please write different title.")
            if e.diag.message_primary.find("post_text") > 0 & e.diag.message_primary.find("unique"):
                errList.append("This content is created before. Please check and re-create the post.")
            return jsonify({'status' : 'FAIL',
                            'errcode' : e.pgcode,
                            'errmsg' : errList
                            })

        return jsonify({
            'status' : 'OK',
            'errcode' : '00000',
            'last_row_id' : lastRowID
            })

@post.route('/posts/<int:post_id>', methods = ['GET', 'POST'])
def get_post(post_id):
    if request.method == 'GET':
        commentServiceObject = CommentService()
        all_comments = commentServiceObject.get_all_comments(post_id)
        postObject = post.service.get_post(post_id)
        return render_template('post.html',postObject = postObject, all_comments = all_comments)
    else:
        if request.json['op'] == "delete_comment":
            commentServiceObject = CommentService()
            try:
                commentServiceObject.delete_comment(request.json['comment_id'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL',
                                'errcode' : e.pgcode,
                                'errmsg' : e.diag.message_primary
                                })

        return jsonify({'status' : 'OK',
                        'errcode' : '00000'
                        })
@post.route('/posts/delete', methods = ['POST'])
def delete_post():
    try:
        post.service.delete_post(request.json['post_id'])
    except dbapi2.Error as e:
        return jsonify({'status' : 'FAIL',
                        'errcode' : e.pgcode
                        })
    return jsonify({'status' : 'OK',
                        'errcode' : '00000'
                    })
@post.route('/posts/edit/<int:post_id>', methods = ['GET', 'POST'])
def update_post(post_id):
    if request.method == 'GET':
        tagServiceObject = TagService()
        all_tags = tagServiceObject.get_all_tags()
        postObject = post.service.get_post(post_id)
        return render_template('edit_post.html', postObject = postObject, all_tags = all_tags)
    else:
        errList = [];
        if getHTMLText(request.json['post_text']) == "":
            errList.append("Post Content cannot be empty!")
        if request.json['tag_id'] == "":
            errList.append("Tag must be assigned!")
        if request.json['title'] == "":
            errList.append("Title cannot be empty!")
        if len(errList) != 0:
            return jsonify({
                'status' : 'FAIL',
                'errmsg': errList
                })
        try:
            post.service.update_post(post_id,request.json['title'],request.json['tag_id'],request.json['post_text'])
        except dbapi2.Error as e:
            if e.diag.message_primary.find("title") > 0 & e.diag.message_primary.find("unique"):
                errList.append("Title is used. Please write different title.")
            if e.diag.message_primary.find("post_text") > 0 & e.diag.message_primary.find("unique"):
                errList.append("This content is created before. Please check and re-create the post.")
            return jsonify({'status' : 'FAIL',
                            'errcode' : e.pgcode,
                            'errmsg' : errList
                            })

        return jsonify({'status' : 'OK',
                        'errcode' : '00000'
                        })

