import psycopg2 as dbapi2

from announcement_class import Announcement
from flask.globals import current_app, request


class AnnouncementService:
    def init_announcement_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE announcements (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            fromuserid INT NOT NULL,
            crt_time TIMESTAMP NOT NULL
        )"""
            cursor.execute(query)
            connection.commit()
    def add_announcement(self,announcement):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO announcements (name,fromuserid,crt_time) VALUES (%s,1,CURRENT_TIMESTAMP) "
             cursor.execute(query,(announcement.name,))
             connection.commit()
    def delete_announcement(self,announcement):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM announcements WHERE name = %s"
            cursor.execute(query,(announcement.name,))
            connection.commit()
    def get_announcement(self,announcement):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM announcements WHERE name = %s"
            cursor.execute(query,(announcement.name,))
            connection.commit()
    def update_announcement(self,announcement):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE announcements SET name = %s"
            cursor.execute(query,(announcement.name,))
            connection.commit()