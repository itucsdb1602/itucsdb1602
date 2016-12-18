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
            fromuserid INT references users(id) ON DELETE CASCADE,
            fromgroupid INT references groups(id) ON DELETE CASCADE,
            crt_time TIMESTAMP NOT NULL
        )"""
            cursor.execute(query)
            connection.commit()
    def add_announcement(self,announcement):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO announcements (name,fromuserid,fromgroupid,crt_time) VALUES (%s,1,3,CURRENT_TIMESTAMP) "
             cursor.execute(query,(announcement.name,))
             connection.commit()

    def get_all_announcements(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name,fromuserid,fromgroupid FROM announcements"
            cursor.execute(query)
            all_announcements = [(key, Announcement(name,fromuserid,fromgroupid))
                        for key,name,fromuserid,fromgroupid in cursor]
            return all_announcements

    def get_announcements_by_name(self,announcement_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name,fromuserid,fromgroupid FROM announcements WHERE name ILIKE %s"
            cursor.execute(query,("%" + announcement_name + "%",))
            announcement_search_result = [Announcement(name,fromuserid,fromgroupid,id = key).json_serialize()
                        for key,name,fromuserid,fromgroupid in cursor]
            return announcement_search_result

    def get_announcement(self,announcement_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name,fromgroupid,fromuserid FROM announcements WHERE id = %s"
            cursor.execute(query,(announcement_id,))
            key,name,fromgroupid,fromuserid = cursor.fetchone()
            return Announcement(name,fromuserid,fromgroupid,id = key)

    def update_announcement(self,announcement_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE announcements SET name = %s, crt_time = CURRENT_TIMESTAMP WHERE id = %s"
            cursor.execute(query,(input_name,announcement_id,))
            connection.commit()

    def delete_announcement(self,announcement_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM announcements WHERE id = %s"
            cursor.execute(query,(announcement_id,))
            connection.commit()
