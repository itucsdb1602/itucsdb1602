import psycopg2 as dbapi2

from announcement_class import Announcement
from flask.globals import current_app, request


class AnnouncementService:
    def add_announcement(self,announcement):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO announcements (name,fromuserid,crt_time) VALUES (%s,1,CURRENT_TIMESTAMP) "
             cursor.execute(query,(announcement.name,))
             connection.commit()