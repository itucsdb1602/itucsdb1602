Parts Implemented by Özgün Kıvrakdal
====================================


users Table
-----------

- **CREATE**

Creating a user table is operated by create_table() function and all columns with the rows to be ready to filled in being used on proper routes. This initialization is triggered by "Create Users' Table" link under the login or register on navigation bar.
When it is run then this table is initialized in database.

.. code-block:: python

   def create_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
            CREATE TABLE users (
                id bigserial primary key,
                username varchar(40) unique not null,
                email varchar(40) unique not null,
                passwordHash varchar(80) not null,
                fullname varchar(40) not null,
                gender varchar(6) not null
            )
            """
            cursor.execute(query)
            connection.commit()

- **ADD**

Adding users handled in register page

.. code-block:: python

   def register_user(self, user):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO users(username, email, passwordHash, fullname, gender )
                                   VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (user.username, user.email, user.passwordHash, user.fullname, user.gender))
            connection.commit()


- **DELETE**

In the settings page users can delete itself.

.. code-block:: python

   def delete_user(self, id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM users
                       WHERE id = %s
                    """
            cursor.execute(query, (id,))
            connection.commit()



- **UPDATE**

To update, users should go settings page.

.. code-block:: python

   def update_user(self, current_user):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE users SET
                         username = %s,
                         email = %s,
                         passwordHash = %s,
                         fullname = %s,
                         gender = %s
                       WHERE
                         id = %s
                    """
            cursor.execute(query, (current_user.username, current_user.email, current_user.passwordHash, current_user.fullname, current_user.gender, current_user.id))
            connection.commit()


- **get all users**
It is used to lists all the users with all informations in it.


.. code-block:: python

    def search(self, search_query, current_user):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT id, username, email, passwordHash, fullname, gender FROM users
                    WHERE username LIKE %(like)s OR fullname LIKE %(like)s"""
            cursor.execute(query, dict(like= '%'+search_query+'%'))
            users = []
            for user_id, username, email, passwordHash, fullname, gender in cursor:
                user = User(username, email, passwordHash, fullname, gender)
                user.id = user_id
                user.blocked, user.flagged, user.friend, user.closer_friend = False, False, False, False
                if current_user.is_authenticated:
                    user.blocked, user.flagged = block_service.get_state(current_user.id, user.id)
                    user.friend, user.closer_friend = friend_service.get_state(current_user.id, user.id)
                users.append(user)
            return users

- **get user by name**

It is used for the search operations to reach the user by seeking the username.

.. code-block:: python

   def get_user_by_username(self, username):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT id, username, email, passwordHash, fullname, gender FROM users WHERE username = %s"""
            cursor.execute(query, (username,))
            data = cursor.fetchone()
            if data:
                user_id, username, email, passwordHash, fullname, gender = data
                user = User(username, email, passwordHash, fullname, gender)
                user.id = user_id
            else:
                user = None
            return user



users_friend Table
------------------

- **CREATE**

Creation of users_friend table

.. code-block:: python

       def create_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
            CREATE TABLE users_friend (
                user_id bigint not null,
                friend_user_id bigint,
                friend_level smallint not null,
                PRIMARY KEY (user_id, friend_user_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (friend_user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
            cursor.execute(query)
            connection.commit()

- **ADD and UPDATE**

Adding friends_table result to adding another user.


.. code-block:: python

       def add_friend(self, current_user_id, other_user_id, is_new_friend):
        if is_new_friend:
            # insert as level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO users_friend(friend_level, user_id, friend_user_id)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(query, (1, current_user_id, other_user_id))
                connection.commit()
        else:
            # update to level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE users_friend SET
                             friend_level = %s
                           WHERE user_id = %s AND friend_user_id = %s
                        """
                cursor.execute(query, (1, current_user_id, other_user_id))
                connection.commit()

- **DELETE**

When selected friend wants to be unfriend in the following code triggering.

.. code-block:: python

   def unfriend(self, current_user_id, other_user_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM users_friend
                       WHERE user_id = %s AND friend_user_id = %s
                    """
            cursor.execute(query, (current_user_id, other_user_id))
            connection.commit()


- **INSERT**

When users want to update friendship status with another, it handled in make_close_friend


.. code-block:: python

       def make_close_friend(self, current_user_id, other_user_id, is_new_friend):
        if is_new_friend:
            # insert as level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO users_friend(friend_level, user_id, friend_user_id)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(query, (2, current_user_id, other_user_id))
                connection.commit()
        else:
            # update to level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE users_friend SET
                             friend_level = %s
                           WHERE user_id = %s AND friend_user_id = %s
                        """
                cursor.execute(query, (2, current_user_id, other_user_id))
                connection.commit()


- **GET**

It is used for showing state of friendship by taking the unique ids' of the users.

.. code-block:: python

   def get_state(self, current_user_id, other_user_id):
        level = 0
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT friend_level FROM users_friend WHERE user_id = %s AND friend_user_id = %s"""
            cursor.execute(query, (current_user_id, other_user_id))
            connection.commit()
            level = cursor.fetchone()
        if not level:
            return False, False
        elif level[0] == 1:
            return True, False
        elif level[0] == 2:
            return True, True


- **List friends**

This is used to display users' friends.

.. code-block:: python

   def list_friends(self, current_user):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT id, username, email, passwordHash, fullname, gender FROM users
                    WHERE id IN (SELECT friend_user_id FROM users_friend WHERE user_id = %s)"""
            cursor.execute(query, (current_user.id,))
            users = []
            for user_id, username, email, passwordHash, fullname, gender in cursor:
                user = User(username, email, passwordHash, fullname, gender)
                user.id = user_id
                user.blocked, user.flagged, user.friend, user.closer_friend = False, False, False, False
                if current_user.is_authenticated:
                    user.blocked, user.flagged = block_service.get_state(current_user.id, user.id)
                    user.friend, user.closer_friend = self.get_state(current_user.id, user.id)
                users.append(user)
            return users



users_block Table
-----------------

- **CREATE**

To create a users_block table one again create_table is used.

.. code-block:: python

    def create_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """
            CREATE TABLE users_block (
                user_id bigint not null,
                blocked_user_id bigint not null,
                block_level smallint not null,
                PRIMARY KEY (user_id, blocked_user_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (blocked_user_id) REFERENCES users (id) ON DELETE CASCADE
            )
            """
            cursor.execute(query)
            connection.commit()

- **ADD and UPDATE**

If user wants to block another one, it triggers block function. Users can flag as an inappropriate before block.

.. code-block:: python

    def block(self, current_user_id, other_user_id, is_new_block):
        if is_new_block:
            # insert as level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO users_block(block_level, user_id, blocked_user_id)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(query, (1, current_user_id, other_user_id))
                connection.commit()
        else:
            # update to level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE users_block SET
                             block_level = %s
                           WHERE user_id = %s AND blocked_user_id = %s
                        """
                cursor.execute(query, (1, current_user_id, other_user_id))
                connection.commit()

Users can flag as an inappropriate before block.

.. code-block:: python

   def flag(self, current_user_id, other_user_id, is_new_block):
        if is_new_block:
            # insert as level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO users_block(block_level, user_id, blocked_user_id)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(query, (2, current_user_id, other_user_id))
                connection.commit()
        else:
            # update to level 1
            with dbapi2.connect(current_app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE users_block SET
                             block_level = %s
                           WHERE user_id = %s AND blocked_user_id = %s
                        """
                cursor.execute(query, (2, current_user_id, other_user_id))
                connection.commit()

- **DELETE**

Table can be dropped immediately with this function.

.. code-block:: python

   def destroy_table(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DROP TABLE users_block CASCADE"""
            cursor.execute(query)
            connection.commit()


- **get state**

This part is used to display the block levels.

.. code-block:: python

    def get_state(self, current_user_id, other_user_id):
        level = 0
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT block_level FROM users_block WHERE user_id = %s AND blocked_user_id = %s"""
            cursor.execute(query, (current_user_id, other_user_id))
            connection.commit()
            level = cursor.fetchone()
            print(level)
        if not level:
            return False, False
        elif level[0] == 1:
            return True, False
        elif level[0] == 2:
            return True, True