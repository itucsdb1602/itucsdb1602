import psycopg2 as dbapi2
from flask import Blueprint, render_template, url_for , redirect, request
from flask.globals import current_app, request
from user_service import UserService
from user_class import User
from crypt import methods

user = Blueprint('user',__name__)
user.service = UserService()

@user.route('/user/init')
def init_user_database():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE users (
            id bigserial primary key,
            username varchar(20) unique not null,
            email varchar(40) unique not null,
            password bytea not null,
            full_name varchar(40) not null,
            gender char,
            isBlocked char not null
        )"""
        cursor.execute(query)
        connection.commit()
        return render_template('home.html',**locals())
@user.route('/ozgun', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('ozgun.html')
    else:

        userObject = User(request.form['reg_username'], request.form['reg_email'], request.form['reg_password'],
                          request.form['reg_fullname'], 'F','F')
        user.service.add_user(userObject.username,userObject.email,userObject.password,userObject.fullname,'F','F')
        return render_template('home.html')


