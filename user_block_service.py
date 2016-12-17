import psycopg2 as dbapi2
from user_class import User
from flask.globals import current_app, request

class UserBlockService(object):
    def create_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
            CREATE TABLE users_block (
                user_id bigint not null,
                blocked_user_id bigint not null,
                block_level smallint not null,
                PRIMARY KEY (user_id, blocked_user_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (blocked_user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
            cursor.execute(query)
            connection.commit()

    def destroy_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DROP TABLE users_block CASCADE"""
            cursor.execute(query)
            connection.commit()


    def get_state(self, current_user_id, other_user_id):
        level = 0
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT block_level FROM users_block WHERE user_id = %s AND blocked_user_id = %s"""
            cursor.execute(query, (current_user_id, other_user_id))
            connection.commit()
            level = cursor.fetchone()
            print(level)
        if not level:
            return False, False
        elif level[0] == 1:
            return True, False
        elif level[0] == 2:
            return True, True

    def block(self, current_user_id, other_user_id, is_new_block):
        if is_new_block:
            # insert as level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO users_block(block_level, user_id, blocked_user_id)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(query, (1, current_user_id, other_user_id))
                connection.commit()
        else:
            # update to level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE users_block SET
                             block_level = %s
                           WHERE user_id = %s AND blocked_user_id = %s
                        """
                cursor.execute(query, (1, current_user_id, other_user_id))
                connection.commit()

    def flag(self, current_user_id, other_user_id, is_new_block):
        if is_new_block:
            # insert as level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO users_block(block_level, user_id, blocked_user_id)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(query, (2, current_user_id, other_user_id))
                connection.commit()
        else:
            # update to level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE users_block SET
                             block_level = %s
                           WHERE user_id = %s AND blocked_user_id = %s
                        """
                cursor.execute(query, (2, current_user_id, other_user_id))
                connection.commit()

    def unblock(self, current_user_id, other_user_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM users_block
                       WHERE user_id = %s AND blocked_user_id = %s
                    """
            cursor.execute(query, (current_user_id, other_user_id))
            connection.commit()