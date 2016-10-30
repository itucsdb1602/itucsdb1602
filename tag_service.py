import psycopg2 as dbapi2

from tag_class import Tag
from flask.globals import current_app, request


class TagService:
    def init_tag_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE tags (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )"""
            cursor.execute(query)
            connection.commit()
    def add_tag(self,tag):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO tags (name) VALUES (%s)"
             cursor.execute(query,(tag.name,))
             connection.commit()

    def get_all_tags(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tags"
            cursor.execute(query)
            all_tags = [(key, Tag(name))
                        for key,name in cursor]
            return all_tags
