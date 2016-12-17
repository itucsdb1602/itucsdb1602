import psycopg2 as dbapi2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, url_for , redirect, request, flash
from flask.globals import current_app, request
from flask_login import login_required, logout_user, login_user, current_user

from user_friend_service import UserFriendService

user_friend = Blueprint('user_friend', __name__)
user_friend.service = UserFriendService()

@user_friend.errorhandler(dbapi2.Error)
def database_exception_handler(error):
    return 'Database error: '+str(error), 500

@user_friend.route('/friends')
def friends():
    users = user_friend.service.list_friends(current_user)
    return render_template('users.html', users=users)

@user_friend.route('/users/<user_id>/friend')
@login_required
def add_friend(user_id):
    is_new_friend = request.args.get('is_new')
    # Default is True
    if is_new_friend == None:
        is_new_friend = True
    else:
        is_new_friend = is_new_friend == '1'
    user_friend.service.add_friend(current_user.id, user_id, is_new_friend)
    return redirect(request.referrer + "#" + str(user_id))

@user_friend.route('/users/<user_id>/closer')
@login_required
def make_close_friend(user_id):
    is_new_friend = request.args.get('is_new')
    # Default is True
    if is_new_friend == None:
        is_new_friend = True
    else:
        is_new_friend = is_new_friend == '1'
    user_friend.service.make_close_friend(current_user.id, user_id, is_new_friend)
    return redirect(request.referrer + "#" + str(user_id))

@user_friend.route('/users/<user_id>/unfriend')
@login_required
def unfriend(user_id):
    user_friend.service.unfriend(current_user.id, user_id)
    return redirect(request.referrer + "#" + str(user_id))