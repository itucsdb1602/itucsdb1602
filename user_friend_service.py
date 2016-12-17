import psycopg2 as dbapi2
from user_class import User
from flask.globals import current_app, request

from user_block_service import UserBlockService
block_service = UserBlockService()

class UserFriendService(object):
    def create_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
            CREATE TABLE users_friend (
                user_id bigint not null,
                friend_user_id bigint,
                friend_level smallint not null,
                PRIMARY KEY (user_id, friend_user_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (friend_user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
            cursor.execute(query)
            connection.commit()

    def destroy_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DROP TABLE users_friend CASCADE"""
            cursor.execute(query)
            connection.commit()

    def list_friends(self, current_user):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT id, username, email, passwordHash, fullname, gender FROM users
                    WHERE id IN (SELECT friend_user_id FROM users_friend WHERE user_id = %s)"""
            cursor.execute(query, (current_user.id,))
            users = []
            for user_id, username, email, passwordHash, fullname, gender in cursor:
                user = User(username, email, passwordHash, fullname, gender)
                user.id = user_id
                user.blocked, user.flagged, user.friend, user.closer_friend = False, False, False, False
                if current_user.is_authenticated:
                    user.blocked, user.flagged = block_service.get_state(current_user.id, user.id)
                    user.friend, user.closer_friend = self.get_state(current_user.id, user.id)
                users.append(user)
            return users

    def get_state(self, current_user_id, other_user_id):
        level = 0
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT friend_level FROM users_friend WHERE user_id = %s AND friend_user_id = %s"""
            cursor.execute(query, (current_user_id, other_user_id))
            connection.commit()
            level = cursor.fetchone()
        if not level:
            return False, False
        elif level[0] == 1:
            return True, False
        elif level[0] == 2:
            return True, True

    def add_friend(self, current_user_id, other_user_id, is_new_friend):
        if is_new_friend:
            # insert as level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO users_friend(friend_level, user_id, friend_user_id)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(query, (1, current_user_id, other_user_id))
                connection.commit()
        else:
            # update to level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE users_friend SET
                             friend_level = %s
                           WHERE user_id = %s AND friend_user_id = %s
                        """
                cursor.execute(query, (1, current_user_id, other_user_id))
                connection.commit()

    def make_close_friend(self, current_user_id, other_user_id, is_new_friend):
        if is_new_friend:
            # insert as level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO users_friend(friend_level, user_id, friend_user_id)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(query, (2, current_user_id, other_user_id))
                connection.commit()
        else:
            # update to level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE users_friend SET
                             friend_level = %s
                           WHERE user_id = %s AND friend_user_id = %s
                        """
                cursor.execute(query, (2, current_user_id, other_user_id))
                connection.commit()

    def unfriend(self, current_user_id, other_user_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM users_friend
                       WHERE user_id = %s AND friend_user_id = %s
                    """
            cursor.execute(query, (current_user_id, other_user_id))
            connection.commit()