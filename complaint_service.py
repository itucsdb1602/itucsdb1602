import psycopg2 as dbapi2

from complaint_class import Complaint
from flask.globals import current_app, request


class ComplaintService:
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

    def add_complaint(self,complaint):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO complaint ( complaint_text,complaint_object,complaint_object_id,crt_id, crt_time,is_done ) VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP,0)"
            cursor.execute(query,(complaint.complaint_text,complaint.complaint_object,complaint.complaint_object_id,complaint.crt_id))
            connection.commit()

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

    def delete_complaint(self,complaint_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM complaint WHERE id = %s"
            cursor.execute(query,(complaint_id,))
            connection.commit()

    def update_complaint(self,complaint_id):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE complaint SET is_done = 1 WHERE id = %s"
            cursor.execute(query,(complaint_id,))
            connection.commit()
