import psycopg2 as dbapi2

from tag_class import Tag
from flask.globals import current_app, request


class TagService:
    def add_tag(self,tag):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO tags (name) VALUES (%s)"
             cursor.execute(query,(tag.name,))
             connection.commit()
