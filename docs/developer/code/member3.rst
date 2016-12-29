Parts Implemented by SAMET YILMAZ
=================================

      In this project,as a PostIT, we have 3 table "*Keywords*", "*Post_keywords*" and "*User_subs*".



Keywords
--------

Create Keywords
~~~~~~~~~~~~~~~
   Initilazion of Keywords table.

.. code-block:: python

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
..


Add Keywords
~~~~~~~~~~~~

Adding keywords to keywords table.

.. code-block:: python

   def add_keywords(self,Keywords):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO keywordss (name,tag_id) VALUES (%s,%s)"
             cursor.execute(query,(Keywords.name,Keywords.tag_id))
             connection.commit()
..



Delete Keywords
~~~~~~~~~~~~~~~

Delete keywords from keywords table.

.. code-block:: python

     def delete_keywords(self,keywords_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM keywordss WHERE id = %s"
            cursor.execute(query,(keywords_id,))
            connection.commit()

..


Update Keywords
~~~~~~~~~~~~~~~

   Update choosen keywords value.

.. code-block:: python

     def update_keywords(self,keywords_id,tag_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE keywordss SET name = %s, tag_id = %s WHERE id = %s"
            cursor.execute(query,(input_name,tag_id,keywords_id))
            connection.commit()

..

   In this request we controlled if user choose a player before delete.


Search Keywords
~~~~~~~~~~~~~~~

   Search keywords by keywords name.

.. code-block:: python

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

..

Get tags Keywords
~~~~~~~~~~~~~~~~~

    Get keywords by choosen tag.

.. code-block:: python

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

..


Post Keywords
-------------

Create Post Keywords
~~~~~~~~~~~~~~~~~~~~

   Initilazion of Post Keywords table.

.. code-block:: python

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
..


Add Post Keywords
~~~~~~~~~~~~~~~~~

Adding keywords to Post Keywords table.
.. code-block:: python

   def add_post_keywords(self, PostKeywords):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO pKeywordss (keywords_id,post_id) VALUES (%s,%s)"
             cursor.execute(query,(PostKeywords.keywords_id,PostKeywords.post_id))
             connection.commit()
..



Delete Post Keywords
~~~~~~~~~~~~~~~~~~~~

Delete keywords from Post Keywords table.

.. code-block:: python

     def delete_post_keywords(self,PostKeywords):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM pKeywordss WHERE post_id = %s AND keywords_id = %s"
            cursor.execute(query,(PostKeywords.post_id,PostKeywords.keywords_id))
            connection.commit()

..

   In this request we controlled if user choose a player before delete.


Search All Post Keywords
~~~~~~~~~~~~~~~~~~~~~~~~

   Search All Post Keywords by Post Id.

.. code-block:: python

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

..



User Subs
---------

Create User Subs
~~~~~~~~~~~~~~~~

    Initilazion of User Subs table.

.. code-block:: python

    def init_user_subs_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE uSubs (
                user_id SERIAL NOT NULL,
                tag_id SERIAL NOT NULL,
                PRIMARY KEY (user_id,tag_id),
                FOREIGN KEY (tag_id) REFERENCES posts (id)
                    ON DELETE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()
..


Add User Subs
~~~~~~~~~~~~~

Adding user to User Subs table.

.. code-block:: python

   def add_user_subs(self, UserSubs):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO uSubs (user_id,tag_id) VALUES (%s,%s)"
             cursor.execute(query,(UserSubs.user_id,UserSubs.tag_id))
             connection.commit()

..



Delete User Subs
~~~~~~~~~~~~~~~~

Delete user from User Subs table.

.. code-block:: python

    def delete_user_subs(self,UserSubs):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM uSubs WHERE tag_id = %s AND user_id = %s"
            cursor.execute(query,(UserSubs.tag_id,UserSubs.user_id))
            connection.commit()

..

   In this request we controlled if user choose a player before delete.


Search User Subs
~~~~~~~~~~~~~~~~

   Search user  by tag id.

.. code-block:: python

      def get_all_user_subs(self,tag_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT COUNT(user_id) FROM uSubs WHERE tag_id = %s"
            cursor.execute(query,(tag_id,))
            all_user_subss = cursor.fetchone()[0]
            return all_user_subss


..







