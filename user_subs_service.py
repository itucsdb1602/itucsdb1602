import psycopg2 as dbapi2

from user_subs_class import UserSubs
from flask.globals import current_app, request


class UserSubsService:
    def init_user_subs_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE uSubs (
                user_id SERIAL NOT NULL,
                tag_id SERIAL NOT NULL,
                PRIMARY KEY (user_id,tag_id),
                FOREIGN KEY (tag_id) REFERENCES posts (id)
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()
    def add_user_subs(self, UserSubs):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO uSubs (user_id,tag_id) VALUES (%s,%s)"
             cursor.execute(query,(UserSubs.user_id,UserSubs.tag_id))
             connection.commit()

    def get_all_user_subs(self,tag_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT(user_id) FROM uSubs WHERE tag_id = %s"
            cursor.execute(query,(tag_id,))
            all_user_subss = cursor.fetchone()[0]
            return all_user_subss

    def delete_user_subs(self,UserSubs):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM uSubs WHERE tag_id = %s AND user_id = %s"
            cursor.execute(query,(UserSubs.tag_id,UserSubs.user_id))
            connection.commit()
