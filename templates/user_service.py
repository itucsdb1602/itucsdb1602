import psycopg2 as dbapi2
from user_class import User
from flask.globals import current_app, request

from user_friend_service import UserFriendService
from user_block_service import UserBlockService

friend_service = UserFriendService()
block_service = UserBlockService()

class UserService(object):
    def create_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
            CREATE TABLE users (
                id bigserial primary key,
                username varchar(40) unique not null,
                email varchar(40) unique not null,
                passwordHash varchar(80) not null,
                fullname varchar(40) not null,
                gender varchar(6) not null
            )
            """
            cursor.execute(query)
            connection.commit()

    def destroy_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DROP TABLE users CASCADE"""
            cursor.execute(query)
            connection.commit()

    def register_user(self, user):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO users(username, email, passwordHash, fullname, gender )
                                   VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (user.username, user.email, user.passwordHash, user.fullname, user.gender))
            connection.commit()

    def get_user_by_id(self, user_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT id, username, email, passwordHash, fullname, gender FROM users WHERE id = %s"""
            try:
                cursor.execute(query, (user_id,))
            except dbapi2.Error as e:
                return None
            data = cursor.fetchone()
            if data:
                user_id, username, email, passwordHash, fullname, gender = data
                user = User(username, email, passwordHash, fullname, gender)
                user.id = user_id
            else:
                user = None
            return user

    def get_user_by_username(self, username):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT id, username, email, passwordHash, fullname, gender FROM users WHERE username = %s"""
            cursor.execute(query, (username,))
            data = cursor.fetchone()
            if data:
                user_id, username, email, passwordHash, fullname, gender = data
                user = User(username, email, passwordHash, fullname, gender)
                user.id = user_id
            else:
                user = None
            return user

    def list_all_users(self, current_user):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT id, username, email, passwordHash, fullname, gender FROM users"""
            cursor.execute(query)
            users = []
            for user_id, username, email, passwordHash, fullname, gender in cursor:
                user = User(username, email, passwordHash, fullname, gender)
                user.id = user_id
                user.blocked, user.flagged, user.friend, user.closer_friend = False, False, False, False
                if current_user.is_authenticated:
                    user.blocked, user.flagged = block_service.get_state(current_user.id, user.id)
                    user.friend, user.closer_friend = friend_service.get_state(current_user.id, user.id)
                users.append(user)
            return users

    def update_user(self, current_user):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE users SET
                         username = %s,
                         email = %s,
                         passwordHash = %s,
                         fullname = %s,
                         gender = %s
                       WHERE
                         id = %s
                    """
            cursor.execute(query, (current_user.username, current_user.email, current_user.passwordHash, current_user.fullname, current_user.gender, current_user.id))
            connection.commit()

    def delete_user(self, id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM users
                       WHERE id = %s
                    """
            cursor.execute(query, (id,))
            connection.commit()