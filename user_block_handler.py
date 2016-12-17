import psycopg2 as dbapi2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, url_for , redirect, request, flash
from flask.globals import current_app, request
from flask_login import login_required, logout_user, login_user, current_user

from user_block_service import UserBlockService

user_block = Blueprint('user_block', __name__)
user_block.service = UserBlockService()

@user_block.errorhandler(dbapi2.Error)
def database_exception_handler(error):
    return 'Database error: '+str(error), 500

@user_block.route('/users/<user_id>/block')
@login_required
def block(user_id):
    is_new_block = request.args.get('is_new')
    # Default is True
    if is_new_block == None:
        is_new_block = True
    else:
        is_new_block = is_new_block == '1'
    user_block.service.block(current_user.id, user_id, is_new_block)
    return redirect(request.referrer + "#" + str(user_id))

@user_block.route('/users/<user_id>/flag')
@login_required
def flag(user_id):
    is_new_block = request.args.get('is_new')
    # Default is True
    if is_new_block == None:
        is_new_block = True
    else:
        is_new_block = is_new_block == '1'
    user_block.service.flag(current_user.id, user_id, is_new_block)
    return redirect(request.referrer + "#" + str(user_id))

@user_block.route('/users/<user_id>/unblock')
@login_required
def unblock(user_id):
    user_block.service.unblock(current_user.id, user_id)
    return redirect(request.referrer + "#" + str(user_id))