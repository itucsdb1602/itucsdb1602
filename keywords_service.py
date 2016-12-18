import psycopg2 as dbapi2

from keywords_class import Keywords
from flask.globals import current_app, request

class keywordsService:
    def init_keywords_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE keywordss (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                tag_id INT NOT NULL
            )"""
            cursor.execute(query)
            connection.commit()
    def add_keywords(self,Keywords):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO keywordss (name,tag_id) VALUES (%s,%s)"
             cursor.execute(query,(Keywords.name,Keywords.tag_id))
             connection.commit()

    def get_all_keywordss(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT keywordss.id, keywordss.name, keywordss.tag_id, tags.name AS tag_name FROM keywordss
                        LEFT JOIN tags ON keywordss.tag_id = tags.id"""
            cursor.execute(query)
            all_keywordss = [(key, Keywords(name,tag_id,tag_name = tag_name))
                        for key,name,tag_id,tag_name in cursor]
            return all_keywordss
    def get_keywordss_by_name(self,keywords_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT keywordss.id, keywordss.name, keywordss.tag_id, tags.name AS tag_name FROM keywordss
                        LEFT JOIN tags ON keywordss.tag_id = tags.id
                         WHERE keywordss.name ILIKE %s"""
            cursor.execute(query,("%" + keywords_name + "%",))
            keywords_search_result = [Keywords(name,tag_id,id = key, tag_name = tag_name).json_serialize()
                        for key,name,tag_id,tag_name in cursor]
            return keywords_search_result

    def get_keywordss_by_tag_id(self,tag_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT keywordss.id, keywordss.name, keywordss.tag_id FROM keywordss
                        LEFT JOIN tags ON keywordss.tag_id = tags.id
                         WHERE keywordss.tag_id = %s"""
            cursor.execute(query,(tag_id,))
            keywords_search_result = [Keywords(name,tag_id,id = key).json_serialize()
                        for key,name,tag_id in cursor]
            return keywords_search_result

    def get_keywords(self,keywords_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM keywordss WHERE id = %s"
            cursor.execute(query,(keywords_id,))
            key,name,tag_id = cursor.fetchone()
            return Keywords(name,tag_id,id = key)

    def update_keywords(self,keywords_id,tag_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE keywordss SET name = %s, tag_id = %s WHERE id = %s"
            cursor.execute(query,(input_name,tag_id,keywords_id))
            connection.commit()

    def delete_keywords(self,keywords_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM keywordss WHERE id = %s"
            cursor.execute(query,(keywords_id,))
            connection.commit()
