import psycopg2 as dbapi2

from group_class import Group
from flask.globals import current_app, request

class GroupService:
    def init_group_tbl(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE groups (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )"""
            cursor.execute(query)
            connection.commit()
    def add_group(self,group):
         with dbapi2.connect(current_app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "INSERT INTO groups (name) VALUES (%s) "
             cursor.execute(query,(group.name,))
             connection.commit()
    #for groups.html
    def get_all_groups(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name FROM groups"
            cursor.execute(query)
            all_groups = [(key, Group(name,))
                        for key,name in cursor]
            return all_groups

    def get_group(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT id,name FROM groups WHERE id = %s"
            cursor.execute(query,(group_id,))
            key,name = cursor.fetchone()
            return Group(name,key)

    def get_groupname_by_id(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT name FROM groups WHERE id = %s"
            cursor.execute(query,(group_id,))
            name = cursor.fetchone()[0]
            return name

    def get_group_by_name(self,group_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM groups WHERE name ILIKE %s"
            cursor.execute(query,("%" + group_name + "%",))
            group_search_result = [Group(name,key).json_serialize()
                        for key,name in cursor]
            return group_search_result

    def update_group(self,group_id,input_name):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE groups SET name = %s WHERE id = %s"
            cursor.execute(query,(input_name,group_id))
            connection.commit()

    def delete_group(self,group_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM groups WHERE id = %s"
            cursor.execute(query,(group_id,))
            connection.commit()
