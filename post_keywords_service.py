import psycopg2 as dbapi2

from post_keywords_class import PostKeywords
from keywords_class import Keywords
from flask.globals import current_app, request


class PostKeywrodsService:
    def init_post_keywords_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE pKeywordss (
                keywords_id SERIAL NOT NULL,
                post_id SERIAL NOT NULL,
                PRIMARY KEY (keywords_id,post_id),
                FOREIGN KEY (post_id) REFERENCES posts (id)
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()
    def add_post_keywords(self, PostKeywords):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO pKeywordss (keywords_id,post_id) VALUES (%s,%s)"
             cursor.execute(query,(PostKeywords.keywords_id,PostKeywords.post_id))
             connection.commit()

    def get_all_post_keywords(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT keywordss.id ,keywordss.name FROM pKeywordss
                        LEFT JOIN keywordss ON pkeywordss.keywords_id = keywordss.id
                         WHERE post_id = %s"""
            cursor.execute(query,(post_id,))
            all_post_keywords = [Keywords(keywords_name,None,id = keywords_id)
                        for keywords_id, keywords_name in cursor]
            return all_post_keywords

    def delete_post_keywords(self,PostKeywords):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM pKeywordss WHERE post_id = %s AND keywords_id = %s"
            cursor.execute(query,(PostKeywords.post_id,PostKeywords.keywords_id))
            connection.commit()
