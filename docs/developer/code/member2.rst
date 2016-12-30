Parts Implemented by Göktürk GÖK
================================


Complaints Table
----------------

- **CREATE**

Creating a complaint table is operated by init_complaint() function and all columns with the rows to be ready to filled in being used on proper routes. This initialization is triggered by "Create Complaint Table" link under the Göktürk on navigation bar.
When it is run then this table is initialized in database.

.. code-block:: python

   def init_complaint_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE complaint (
                id SERIAL PRIMARY KEY,
                complaint_text TEXT UNIQUE NOT NULL,
                complaint_object TEXT NOT NULL,
                complaint_object_id INT NOT NULL,
                crt_id INT NOT NULL,
                crt_time TIMESTAMP NOT NULL,
                is_done INT NOT NULL,
                FOREIGN KEY (crt_id) REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()

**ADD**

Adding complaint requires the existance of the complaint table to execute the add operation properly and it is triggered by clicking the complaint icon below the name of the owner of the post/comment

.. code-block:: python

   def add_complaint(self,complaint):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO complaint ( complaint_text,complaint_object,complaint_object_id,crt_id, crt_time,is_done ) VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP,0)"
            cursor.execute(query,(complaint.complaint_text,complaint.complaint_object,complaint.complaint_object_id,complaint.crt_id))
            connection.commit()


- **DELETE**
When the selected complaint is wanted to delete then this function takes the is of the complaint which is desired to remove, then deletes the row which takes the id of the complaint properly.
This operation is triggerred from the delete button on the complaint row.

.. code-block:: python

   def delete_complaint(self,complaint_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM complaint WHERE id = %s"
            cursor.execute(query,(complaint_id,))
            connection.commit()


-
- **UPDATE**

To execute the update function, complaint_id should be selected to be operated and it is routed to directly related post or comment which is evaluated by the complaint_handler

.. code-block:: python

   def update_complaint(self,complaint_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE complaint SET is_done = 1 WHERE id = %s"
            cursor.execute(query,(complaint_id,))
            connection.commit()


- **GET_ALL_Complaints**
It is used to lists all the complaints with all informations in it.
.. code-block:: python

    def get_all_complaints(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT complaint.id, complaint.complaint_text, complaint.complaint_object, complaint.complaint_object_id,complaint.crt_id, complaint.crt_time, users.username, complaint.is_done
                        FROM complaint
                        LEFT JOIN users ON complaint.crt_id = users.id
                                """
            cursor.execute(query)
            all_complaints = [(key, Complaint(complaint_text, complaint_object, complaint_object_id, crt_id, crt_username = username, crt_time = crt_time,is_done = is_done))
                        for key,complaint_text, complaint_object, complaint_object_id, crt_id, crt_time, username,is_done in cursor]
            return all_complaints

- **GET_Complaints_by_name**

It is used for the search operations to reach the complaint by seeking the name.

.. code-block:: python

   def get_complaints_by_name(self,complaint_text):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT complaint.id, complaint.complaint_text, complaint.complaint_object, complaint.complaint_object_id,complaint.crt_id, complaint.crt_time, users.username, complaint.is_done
                        FROM complaint
                        LEFT JOIN users ON complaint.crt_id = users.id WHERE complaint.complaint_text ILIKE %s"""
            cursor.execute(query,("%" + complaint_text + "%",))
            complaints_search_result = [Complaint(complaint_text, complaint_object, complaint_object_id, crt_id, crt_username = username, crt_time = crt_time,is_done = is_done, id = key).json_serialize()
                        for key,complaint_text, complaint_object, complaint_object_id, crt_id, crt_time, username,is_done in cursor]
            return complaints_search_result



Comments Table
--------------

- **CREATE**

Creating a comment table is operated by init_comment() function and all columns with the rows to be ready to filled in being used on proper routes. This initialization is triggered by "Create Comment Table" link under the Göktürk on navigation bar.
When it is run then this table is initialized in database.

.. code-block:: python

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
                    ON DELETE CASCADE,
                FOREIGN KEY (crt_id) REFERENCES users (id)
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()

- **ADD**

Adding comment requires the existence of the comment table to execute the add operation properly and it is triggered by clicking the Add Comment button below the related post as ready.


.. code-block:: python

       def add_comment(self,comment):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO comments ( comment_text, post_id, crt_id, crt_time ) VALUES (%s,%s,%s,CURRENT_TIMESTAMP)"
            cursor.execute(query,(comment.comment_text,comment.post_id,comment.crt_id))
            connection.commit()

- **DELETE**

When the selected comment is wanted to delete then this function takes the comment_id which is desired to remove, then deletes the row which takes the id of the comment properly.
This operation is triggerred from the delete button on the comment.

.. code-block:: python

    def delete_comment(self,comment_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM comments WHERE id = %s"
            cursor.execute(query,(comment_id,))
            connection.commit()


- **UPDATE**

To execute the update function, comment_id and comment_text which is going to be changed should be selected to be operated and it is routed to directly related comment's update page which is evaluated by the comment_handler.


.. code-block:: python

       def update_comment(self,comment_id,comment_text):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE comments SET comment_text = %s, upd_id = 1, upd_time = CURRENT_TIMESTAMP WHERE id = %s"
            cursor.execute(query,(comment_text,comment_id))
            connection.commit()


- **GET**

.. code-block:: python

It is used for listing by taking the unique ids' of the comments.


   def get_comment(self,comment_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT comments.id, comments.comment_text, comments.post_id,  comments.crt_id, comments.crt_time,
                        comments.upd_id, comments.upd_time
                            FROM comments WHERE comments.id = %s """

            cursor.execute(query,(comment_id,))
            key,comment_text, post_id, crt_id, crt_time, upd_id, upd_time =  cursor.fetchone()
            return Comment(comment_text ,post_id , crt_id = crt_id, crt_time = crt_time, upd_id = upd_id, upd_time = upd_time, id = key)


- **GET_comment_counter**

This is used to display on number of comments button as the number of comments.

.. code-block:: python

   def get_comment_counter(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT COUNT(id)
                            FROM comments WHERE post_id = %s
                                """
            cursor.execute(query,(post_id,))
            comment_counter = cursor.fetchone()[0];
            return comment_counter



pLikes (Post Likes) Relation
----------------------------

- **CREATE**

Creating a pLikes table is operated by init_post_like_tbl() function and all columns with the rows to be ready to filled in being used on proper routes. This initialization is triggered by "Create pLike Table" link under the Göktürk on navigation bar.
When it is run then this table is initialized in database.

.. code-block:: python

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

- **ADD**

Adding likes of posts requires the existence of the pLikes table to execute the add operation properly and it is triggered by clicking the yellow like button to also keep the number of like post have below the related post as ready.

.. code-block:: python

    def add_post_like(self, PostLike):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO pLikes (user_id,post_id) VALUES (%s,%s)"
             cursor.execute(query,(PostLike.user_id,PostLike.post_id))
             connection.commit()

- **DELETE**

When the selected like is wanted to delete then this function takes the PostLike object which is desired to remove, then deletes the row which takes the id of the comment properly.
This operation is triggerred from the click the like button which operates by "unlike" on the post.

.. code-block:: python

    def delete_post_like(self,PostLike):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM pLikes WHERE post_id = %s AND user_id = %s"
            cursor.execute(query,(PostLike.post_id,PostLike.user_id))
            connection.commit()


- **Get_all_post_like**

This part is used to display the number of likes post have on the like button on posts.

.. code-block:: python

   def get_all_post_like(self,post_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT(user_id) FROM pLikes WHERE post_id = %s"
            cursor.execute(query,(post_id,))
            all_post_likes = cursor.fetchone()[0]
            return all_post_likes