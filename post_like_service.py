import psycopg2 as dbapi2

from post_like_class import PostLike
from flask.globals import current_app, request


class PostLikeService:
    def init_post_like_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE pLikes (
                user_id SERIAL NOT NULL,
                post_id SERIAL NOT NULL,
                PRIMARY KEY (user_id,post_id),
                FOREIGN KEY (post_id) REFERENCES posts (id)
                    ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (id)
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()
    def add_post_like(self, PostLike):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO pLikes (user_id,post_id) VALUES (%s,%s)"
             cursor.execute(query,(PostLike.user_id,PostLike.post_id))
             connection.commit()

    def get_all_post_like(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT(user_id) FROM pLikes WHERE post_id = %s"
            cursor.execute(query,(post_id,))
            all_post_likes = cursor.fetchone()[0]
            return all_post_likes

    def delete_post_like(self,PostLike):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM pLikes WHERE post_id = %s AND user_id = %s"
            cursor.execute(query,(PostLike.post_id,PostLike.user_id))
            connection.commit()
