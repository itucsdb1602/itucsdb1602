import psycopg2 as dbapi2

from group_user_class import GroupUser
from flask.globals import current_app, request


class GroupUserService:
    def init_group_user_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE gUsers (
                user_id INT NOT NULL,
                group_id INT NOT NULL,
                isAdmin INT NOT NULL,
                PRIMARY KEY (user_id,group_id),
                FOREIGN KEY (group_id) REFERENCES groups (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()
    def add_group_user(self, GroupUser):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO gUsers (user_id,group_id,isAdmin) VALUES (%s,%s,%s)"
             cursor.execute(query,(GroupUser.user_id,GroupUser.group_id,GroupUser.isAdmin))
             connection.commit()

    def get_all_group_user(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT gUsers.user_id, gUsers.group_id, gUsers.isAdmin, users.username FROM gUsers
            LEFT JOIN users ON gUsers.user_id = users.id WHERE gUsers.group_id = %s"""
            cursor.execute(query,(group_id,))
            all_groups_users = [(GroupUser(user_id, group_id, isAdmin,user_name = username))
                        for user_id,group_id,isAdmin, username in cursor]
            return all_groups_users

    def delete_group_user(self,GroupUser):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM gUsers WHERE group_id = %s AND user_id = %s"
            cursor.execute(query,(GroupUser.group_id,GroupUser.user_id))
            connection.commit()