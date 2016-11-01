import psycopg2 as dbapi2

from keywords_class import keywords
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
    def add_keywords(self,keywords):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO keywordss (name) VALUES (%s)"
             cursor.execute(query,(keywords.name,))
             connection.commit()

    def get_all_keywordss(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM keywordss"
            cursor.execute(query)
            all_keywordss = [(key, keywords(name))
                        for key,name in cursor]
            return all_keywordss
