Parts Implemented by Bilal
==========================
Announcement Table
------------------
- **CREATE**

.. code-block:: python

   def init_announcement_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE announcements (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            fromuserid INT references users(id) ON DELETE CASCADE,
            fromgroupid INT references groups(id) ON DELETE CASCADE,
            crt_time TIMESTAMP NOT NULL
        )"""
            cursor.execute(query)
            connection.commit()

- **DELETE**

.. code-block:: python

   def delete_announcement(self,announcement_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM announcements WHERE id = %s"
            cursor.execute(query,(announcement_id,))
            connection.commit()


- **ADD**

.. code-block:: python

   def add_announcement(self,announcement):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO announcements (name,fromuserid,fromgroupid,crt_time) VALUES (%s,1,3,CURRENT_TIMESTAMP) "
             cursor.execute(query,(announcement.name,))
             connection.commit()

- **UPDATE**

.. code-block:: python

   def update_announcement(self,announcement_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE announcements SET name = %s, crt_time = CURRENT_TIMESTAMP WHERE id = %s"
            cursor.execute(query,(input_name,announcement_id,))
            connection.commit()


- **GET_ALL_Announcements**

.. code-block:: python

   def get_all_announcements(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name,fromuserid,fromgroupid FROM announcements"
            cursor.execute(query)
            all_announcements = [(key, Announcement(name,fromuserid,fromgroupid))
                        for key,name,fromuserid,fromgroupid in cursor]
            return all_announcements

- **GET_Announcements_by_name**

.. code-block:: python

   def get_announcements_by_name(self,announcement_name):
       with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name,fromuserid,fromgroupid FROM announcements WHERE name ILIKE %s"
            cursor.execute(query,("%" + announcement_name + "%",))
            announcement_search_result = [Announcement(name,fromuserid,fromgroupid,id = key).json_serialize()
                        for key,name,fromuserid,fromgroupid in cursor]
            return announcement_search_result

- **GET_Announcements**

.. code-block:: python

   def get_announcement(self,announcement_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name,fromgroupid,fromuserid FROM announcements WHERE id = %s"
            cursor.execute(query,(announcement_id,))
            key,name,fromgroupid,fromuserid = cursor.fetchone()
            return Announcement(name,fromuserid,fromgroupid,id = key)

Group Table
-----------

- **CREATE**

.. code-block:: python

       def init_group_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE groups (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )"""
            cursor.execute(query)
            connection.commit()

- **ADD**

.. code-block:: python

       def add_group(self,group):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO groups (name) VALUES (%s) "
             cursor.execute(query,(group.name,))
             connection.commit()

- **DELETE**

.. code-block:: python

    def delete_group(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM groups WHERE id = %s"
            cursor.execute(query,(group_id,))
            connection.commit()


- **UPDATE**

.. code-block:: python

       def update_group(self,group_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE groups SET name = %s WHERE id = %s"
            cursor.execute(query,(input_name,group_id))
            connection.commit()


- **GET**

.. code-block:: python

   def get_group(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name FROM groups WHERE id = %s"
            cursor.execute(query,(group_id,))
            key,name = cursor.fetchone()
            return Group(name,key)

- **GET_groupname_by_id**

.. code-block:: python

   def get_groupname_by_id(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT name FROM groups WHERE id = %s"
            cursor.execute(query,(group_id,))
            name = cursor.fetchone()[0]
            return name

- **Get_group_by_name**

.. code-block:: python

   def get_group_by_name(self,group_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM groups WHERE name ILIKE %s"
            cursor.execute(query,("%" + group_name + "%",))
            group_search_result = [Group(name,key).json_serialize()
                        for key,name in cursor]
            return group_search_result

Group-Users Table
-----------------

- **CREATE**

.. code-block:: python

    def init_group_user_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE gUsers (
                user_id INT NOT NULL,
                group_id INT NOT NULL,
                isAdmin INT NOT NULL,
                PRIMARY KEY (user_id,group_id),
                FOREIGN KEY (group_id) REFERENCES groups (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )"""
            cursor.execute(query)
            connection.commit()

- **ADD**

.. code-block:: python

    def add_group_user(self, GroupUser):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO gUsers (user_id,group_id,isAdmin) VALUES (%s,%s,%s)"
             cursor.execute(query,(GroupUser.user_id,GroupUser.group_id,GroupUser.isAdmin))
             connection.commit()

- **DELETE**

.. code-block:: python

    def delete_group_user(self,GroupUser):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM gUsers WHERE group_id = %s AND user_id = %s"
            cursor.execute(query,(GroupUser.group_id,GroupUser.user_id))
            connection.commit()


- **Get_all_group_user**

.. code-block:: python

   def get_all_group_user(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT gUsers.user_id, gUsers.group_id, gUsers.isAdmin, users.username FROM gUsers
            LEFT JOIN users ON gUsers.user_id = users.id WHERE gUsers.group_id = %s"""
            cursor.execute(query,(group_id,))
            all_groups_users = [(GroupUser(user_id, group_id, isAdmin,user_name = username))
                        for user_id,group_id,isAdmin, username in cursor]
            return all_groups_users