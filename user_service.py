import psycopg2 as dbapi2

from user_class import User
from flask.globals import current_app, request


class UserService:
    def add_user(self,username,email,password,fullname,gender,isBlocked):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """INSERT INTO users(
    username, email, password, full_name, gender, isblocked )
    VALUES (%s, %s,%s, %s, %s, %s)"""
             cursor.execute(query,(username, email,password,fullname,gender,isBlocked))
             connection.commit()
