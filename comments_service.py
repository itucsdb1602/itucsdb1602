import psycopg2 as dbapi2

from comments_class import Comment
from flask.globals import current_app, request


class CommentService:
    def init_comment_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE comments (
                id SERIAL PRIMARY KEY,
                post_id INT NOT NULL,
                comment_text TEXT UNIQUE NOT NULL,
                crt_id INT NOT NULL,
                crt_time TIMESTAMP NOT NULL,
                upd_id INT,
                upd_time TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()

    def add_comment(self,comment):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO comments ( comment_text, post_id, crt_id, crt_time ) VALUES (%s,%s,1,CURRENT_TIMESTAMP)"
            cursor.execute(query,(comment.comment_text,comment.post_id))
            connection.commit()

    def get_all_comments(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT comments.id, comments.comment_text , comments.crt_id, comments.crt_time,
                        comments.upd_id, comments.upd_time
                            FROM comments WHERE post_id = %s
                                """
            cursor.execute(query,(post_id,))
            all_comments = [(key, Comment(comment_text, post_id , crt_id = crt_id, crt_time = crt_time, upd_id = upd_id, upd_time = upd_time))
                        for key,comment_text, crt_id, crt_time, upd_id, upd_time in cursor]
            return all_comments

    def get_comment_counter(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT COUNT(id)
                            FROM comments WHERE post_id = %s
                                """
            cursor.execute(query,(post_id,))
            comment_counter = cursor.fetchone()[0];
            return comment_counter

    def get_comment(self,comment_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT comments.id, comments.comment_text, comments.post_id,  comments.crt_id, comments.crt_time,
                        comments.upd_id, comments.upd_time
                            FROM comments WHERE comments.id = %s """

            cursor.execute(query,(comment_id,))
            key,comment_text, post_id, crt_id, crt_time, upd_id, upd_time =  cursor.fetchone()
            return Comment(comment_text ,post_id , crt_id = crt_id, crt_time = crt_time, upd_id = upd_id, upd_time = upd_time, id = key)

    def delete_comment(self,comment_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM comments WHERE id = %s"
            cursor.execute(query,(comment_id,))
            connection.commit()

    def update_comment(self,comment_id,comment_text):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE comments SET comment_text = %s, upd_id = 1, upd_time = CURRENT_TIMESTAMP WHERE id = %s"
            cursor.execute(query,(comment_text,comment_id))
            connection.commit()
