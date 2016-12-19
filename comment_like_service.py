import psycopg2 as dbapi2

from comment_like_class import CommentLike
from flask.globals import current_app, request


class CommentLikeService:
    def init_comment_like_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE comment_likes (
                user_id SERIAL NOT NULL,
                comment_id SERIAL NOT NULL,
                PRIMARY KEY (user_id,comment_id),
                FOREIGN KEY (comment_id) REFERENCES comments (id)
                    ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (id)
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()
    def add_comment_like(self, CommentLike):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO comment_likes (user_id,comment_id) VALUES (%s,%s)"
             cursor.execute(query,(CommentLike.user_id,CommentLike.comment_id))
             connection.commit()

    def get_all_comment_like(self,comment_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT(user_id) FROM comment_likes WHERE comment_id = %s"
            cursor.execute(query,(comment_id,))
            all_comment_likes = cursor.fetchone()[0]
            return all_comment_likes

    def delete_comment_like(self,CommentLike):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM comment_likes WHERE comment_id = %s AND user_id = %s"
            cursor.execute(query,(CommentLike.comment_id,CommentLike.user_id))
            connection.commit()
