import psycopg2 as dbapi2

from post_class import Post
from flask.globals import current_app, request


class PostService:
    def init_post_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE posts (
                id SERIAL PRIMARY KEY,
                title TEXT UNIQUE NOT NULL,
                post_text TEXT UNIQUE NOT NULL,
                tag_id INT NOT NULL,
                crt_id INT NOT NULL,
                crt_time TIMESTAMP NOT NULL,
                upd_id INT,
                upd_time TIMESTAMP,
                group_id INT,
                FOREIGN KEY (tag_id) REFERENCES tags (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY (crt_id) REFERENCES users (id)
                    ON DELETE CASCADE,
                FOREIGN KEY (upd_id) REFERENCES users (id)
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()

    def add_post(self,post):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO posts (title, post_text, tag_id, crt_id, crt_time ) VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP) RETURNING id"
            cursor.execute(query,(post.title,post.post_text,post.tag_id,post.crt_username))
            connection.commit()
            return cursor.fetchone()[0];

    def get_all_posts(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT posts.id, posts.title, posts.post_text, posts.tag_id, posts.crt_id, posts.crt_time,
                        posts.upd_id, posts.upd_time, posts.group_id, tags.name AS tag_name, users.username AS crt_username
                            FROM posts
                            LEFT JOIN tags ON posts.tag_id = tags.id
                            LEFT JOIN users ON posts.crt_id = users.id"""
            cursor.execute(query)
            all_posts = [(key, Post(post_text, tag_id, title, crt_id = crt_id, crt_time = crt_time, upd_id = upd_id, upd_time = upd_time, group_id = group_id, tag_name = tag_name, crt_username = crt_username))
                        for key,title,post_text,tag_id, crt_id, crt_time, upd_id, upd_time, group_id, tag_name, crt_username in cursor]
            return all_posts

    def get_post(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT posts.id, posts.title, posts.post_text, posts.tag_id, posts.crt_id, posts.crt_time,
                        posts.upd_id, posts.upd_time, posts.group_id, tags.name AS tag_name, users.username AS crt_username
                            FROM posts
                            LEFT JOIN tags ON posts.tag_id = tags.id
                            LEFT JOIN users ON posts.crt_id = users.id
                            WHERE posts.id = %s"""
            cursor.execute(query,(post_id,))
            key,title,post_text,tag_id, crt_id, crt_time, upd_id, upd_time, group_id, tag_name, crt_username =  cursor.fetchone()
            return Post(post_text, tag_id, title, crt_id = crt_id, crt_time = crt_time, upd_id = upd_id, upd_time = upd_time, group_id = group_id, tag_name = tag_name, id = key, crt_username = crt_username)

    def get_all_posts_for_group(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT posts.id, posts.title, posts.post_text, posts.tag_id, posts.crt_id, posts.crt_time,
                        posts.upd_id, posts.upd_time, posts.group_id, tags.name AS tag_name, users.username AS crt_username
                            FROM posts
                            LEFT JOIN tags ON posts.tag_id = tags.id
                            LEFT JOIN users ON posts.crt_id = users.id
                            LEFT JOIN groups ON posts.group_id = groups.id
                            WHERE posts.group_id = %s"""
            cursor.execute(query,(group_id,))
            all_posts = [(key, Post(post_text, tag_id, title, crt_id = crt_id, crt_time = crt_time, upd_id = upd_id, upd_time = upd_time, group_id = group_id, tag_name = tag_name, crt_username = crt_username))
                        for key,title,post_text,tag_id, crt_id, crt_time, upd_id, upd_time, group_id, tag_name, crt_username in cursor]
            return all_posts

    def update_post(self,post_id,title,tag_id,post_text):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE posts SET title = %s, post_text = %s, tag_id = %s, upd_id = 1, upd_time = CURRENT_TIMESTAMP WHERE id = %s"
            cursor.execute(query,(title,post_text,tag_id, post_id))
            connection.commit()

    def delete_post(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM posts WHERE id = %s"
            cursor.execute(query,(post_id,))
            connection.commit()