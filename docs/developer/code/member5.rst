Parts Implemented by Hakan
==========================
Post Table
----------
- **CREATE**

.. code-block:: python

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

- **DELETE**

.. code-block:: python

   def delete_post(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM posts WHERE id = %s"
            cursor.execute(query,(post_id,))
            connection.commit()


- **ADD**

.. code-block:: python

   def add_post(self,post):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO posts (title, post_text, tag_id, crt_id, crt_time ) VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP) RETURNING id"
            cursor.execute(query,(post.title,post.post_text,post.tag_id,post.crt_username))
            connection.commit()
            return cursor.fetchone()[0];

- **UPDATE**

.. code-block:: python

    def update_post(self,post_id,title,tag_id,post_text):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE posts SET title = %s, post_text = %s, tag_id = %s, upd_id = 1, upd_time = CURRENT_TIMESTAMP WHERE id = %s"
            cursor.execute(query,(title,post_text,tag_id, post_id))
            connection.commit()


- **GET ALL POSTS**

.. code-block:: python

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

- **GET POST**

.. code-block:: python

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


- **GET ALL POSTS FOR GROUPS**

.. code-block:: python

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

Tag Table
---------

- **CREATE**

.. code-block:: python

           def init_tag_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE tags (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )"""
            cursor.execute(query)
            connection.commit()

- **ADD**

.. code-block:: python

       def add_tag(self,tag):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO tags (name) VALUES (%s)"
             cursor.execute(query,(tag.name,))
             connection.commit()

- **DELETE**

.. code-block:: python

      def delete_tag(self,tag_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM tags WHERE id = %s"
            cursor.execute(query,(tag_id,))
            connection.commit()


- **UPDATE**

.. code-block:: python

    def update_tag(self,tag_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE tags SET name = %s WHERE id = %s"
            cursor.execute(query,(input_name,tag_id))
            connection.commit()


- **GET TAG**

.. code-block:: python

   def get_tag(self,tag_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tags WHERE id = %s"
            cursor.execute(query,(tag_id,))
            key,title = cursor.fetchone()
            return Tag(title,key)


- **GET TAGS BY NAME**

.. code-block:: python

       def get_tags_by_name(self,tag_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tags WHERE name ILIKE %s"
            cursor.execute(query,("%" + tag_name + "%",))
            tag_search_result = [Tag(name,key).json_serialize()
                        for key,name in cursor]
            return tag_search_result

- **Get_all_tags**

.. code-block:: python

       def get_all_tags(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tags"
            cursor.execute(query)
            all_tags = [(key, Tag(name))
                        for key,name in cursor]
            return all_tags

Comment-likes Table
-------------------

- **CREATE**

.. code-block:: python

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

- **ADD**

.. code-block:: python

    def add_comment_like(self, CommentLike):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO comment_likes (user_id,comment_id) VALUES (%s,%s)"
             cursor.execute(query,(CommentLike.user_id,CommentLike.comment_id))
             connection.commit()

- **DELETE**

.. code-block:: python

    def delete_comment_like(self,CommentLike):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM comment_likes WHERE comment_id = %s AND user_id = %s"
            cursor.execute(query,(CommentLike.comment_id,CommentLike.user_id))
            connection.commit()


- **GET ALL COMMENT LIKES**

.. code-block:: python

       def get_all_comment_like(self,comment_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT(user_id) FROM comment_likes WHERE comment_id = %s"
            cursor.execute(query,(comment_id,))
            all_comment_likes = cursor.fetchone()[0]
            return all_comment_likes