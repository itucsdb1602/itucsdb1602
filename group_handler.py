import psycopg2 as dbapi2
import json
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from group_service import GroupService
from group_user_service import GroupUserService
from group_class import Group
from post_service import PostService
from post_like_service import PostLikeService
from comments_service import CommentService

group = Blueprint('group',__name__)
group.service = GroupService()

@group.route('/group/<int:group_id>')
def group_user(group_id):
    if request.method == 'GET':
        #user_group = gUsers.service.get_all_group_user(group_id)
        groupUserObj = GroupUserService()
        postServiceObj = PostService()
        postLikeServiceObj = PostLikeService()
        commentServiceObj = CommentService()
        group_name = group.service.get_groupname_by_id(group_id)
        delete_user_name = groupUserObj.get_all_group_user(group_id)
        all_posts = postServiceObj.get_all_posts_for_group(group_id)
        all_users = groupUserObj.get_all_group_user(group_id)
        for post_id, postObj in all_posts:
            postObj.post_like = postLikeServiceObj.get_all_post_like(post_id)
            postObj.comment_counter = commentServiceObj.get_comment_counter(post_id)
        return render_template('group.html',all_posts = all_posts,all_users = all_users, group_name = group_name, delete_user_name = delete_user_name)

@group.route('/groups/init')
def init_group_tbl():
    if request.method == 'GET':
        try:
            group.service.init_group_tbl()
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@group.route('/groups/add', methods = ['GET', 'POST'])
def add_group():
    if request.method == 'GET':
        return render_template('add_group.html')
    else:
        groupObject = Group(request.json['name'])
        try:
            group.service.add_group(groupObject)
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})

@group.route('/groups', methods = ['GET', 'POST'])
def get_groups():
    if request.method == 'GET':
        all_groups = group.service.get_all_groups()
        return render_template('groups.html',all_groups = all_groups)
    else:
        if request.json['op'] == 'delete':
            try:
                group.service.delete_group(request.json['group_id'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

            return jsonify({'status' : 'OK', 'errcode' : '00000'})
        elif request.json['op'] == 'search':
            try:
                group_search_result = group.service.get_group_by_name(request.json['group_name'])
            except dbapi2.Error as e:
                return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})
            return jsonify({'status' : 'OK', 'errcode' : '00000', 'data' : group_search_result})

@group.route('/groups/edit/<int:group_id>', methods = ['GET', 'POST'])
def update_group(group_id):
    if request.method == 'GET':
        upd_group = group.service.get_group(group_id)
        return render_template('edit_group.html',upd_group = upd_group);
    else:
        try:
            group.service.update_group(request.json['id'],request.json['name'])
        except dbapi2.Error as e:
            return jsonify({'status' : 'FAIL', 'errcode' : e.pgcode})

        return jsonify({'status' : 'OK', 'errcode' : '00000'})
