import psycopg2 as dbapi2

from keywords_class import Keywords
from flask.globals import current_app, request

class keywordsService:
    def init_keywords_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE keywordss (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )"""
            cursor.execute(query)
            connection.commit()
    def add_keywords(self,Keywords):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO keywordss (name) VALUES (%s)"
             cursor.execute(query,(Keywords.name,))
             connection.commit()

    def get_all_keywordss(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM keywordss"
            cursor.execute(query)
            all_keywordss = [(key, Keywords(name))
                        for key,name in cursor]
            return all_keywordss
    def get_keywordss_by_name(self,keywords_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM keywordss WHERE name ILIKE %s"
            cursor.execute(query,("%" + keywords_name + "%",))
            keywords_search_result = [Keywords(name,key).json_serialize()
                        for key,name in cursor]
            return keywords_search_result
    def get_keywords(self,keywords_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM keywordss WHERE id = %s"
            cursor.execute(query,(keywords_id,))
            key,title = cursor.fetchone()
            return Keywords(title,key)

    def update_keywords(self,keywords_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE keywordss SET name = %s WHERE id = %s"
            cursor.execute(query,(input_name,keywords_id))
            connection.commit()

    def delete_keywords(self,keywords_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM keywordss WHERE id = %s"
            cursor.execute(query,(keywords_id,))
            connection.commit()
