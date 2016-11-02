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

    def get_tags_by_name(self,tag_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tags WHERE name ILIKE %s"
            cursor.execute(query,("%" + tag_name + "%",))
            tag_search_result = [Tag(name,key).json_serialize()
                        for key,name in cursor]
            return tag_search_result
    def get_tag(self,tag_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tags WHERE id = %s"
            cursor.execute(query,(tag_id,))
            key,title = cursor.fetchone()
            return Tag(title,key)

    def update_tag(self,tag_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE tags SET name = %s WHERE id = %s"
            cursor.execute(query,(input_name,tag_id))
            connection.commit()

    def delete_tag(self,tag_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM tags WHERE id = %s"
            cursor.execute(query,(tag_id,))
            connection.commit()
