import psycopg2 as dbapi2
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, url_for , redirect, request, flash
from flask.globals import current_app, request
from flask_login import login_required, logout_user, login_user, current_user
from user_service import UserService
from user_class import User

from user_friend_service import UserFriendService
from user_block_service import UserBlockService

user = Blueprint('user',__name__)
user.service = UserService()
user.friend_service = UserFriendService()
user.block_service = UserBlockService()

@user.errorhandler(dbapi2.Error)
def database_exception_handler(error):
    return 'Database error: '+str(error), 500

@user.route('/users/init')
def init():
    user.service.create_table()
    user.friend_service.create_table()
    user.block_service.create_table()
    return redirect(url_for('home_page'))

@user.route('/users/destroy')
def destroy():
    user.service.destroy_table()
    user.friend_service.destroy_table()
    user.block_service.destroy_table()
    return redirect(url_for('home_page'))

@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    a_user = User(request.form['reg_username'], request.form['reg_email'],
                  generate_password_hash(request.form['reg_password']),
                  request.form['reg_fullname'], request.form['reg_gender'])
    try:
        user.service.register_user(a_user)
    except dbapi2.IntegrityError:
        return render_template('register.html', error="Username or Email is already exist!")
    return redirect(url_for('user.login'))

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    a_user = user.service.get_user_by_username(request.form['lg_username'])
    if a_user and check_password_hash(a_user.passwordHash, request.form['lg_password']):
        remember = False
        if "lg_remember" in request.form:
            remember = True
        print(request.form)
        login_user(a_user, remember=remember)
        return redirect(url_for('home_page'))
    return render_template('login.html', error="Wrong password or username!")

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@user.route('/users')
def list():
    users = user.service.list_all_users(current_user)
    return render_template('users.html', users=users)

@user.route('/search')
def search():
    users = user.service.search(request.args.get('q'), current_user)
    return render_template('users.html', users=users)

@user.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('settings.html')
    current_user.username = request.form['reg_username']
    current_user.email = request.form['reg_email']
    if request.form['reg_password']:
        current_user.passwordHash = generate_password_hash(request.form['reg_password'])
    current_user.fullname = request.form['reg_fullname']
    current_user.gender = request.form['reg_gender']
    try:
        user.service.update_user(current_user)
    except dbapi2.IntegrityError:
        return render_template('settings.html', error="Username or Email is already exist!")
    return render_template('settings.html')

@user.route('/delete')
@login_required
def delete():
    id = current_user.id
    logout_user()
    user.service.delete_user(id)
    return redirect(url_for('home_page'))
