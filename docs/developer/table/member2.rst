Complaints Table
----------------

+------------------+------------+-------------+------------+-------------+-------------+
| Name             | Data Type  | Null Option | Uniqueness | Primary Key | Foreign Key |
+==================+============+=============+============+=============+=============+
| ID               | SERIAL     | NOT NULL    | UNIQUE     | PRIMARY KEY |             |
+------------------+------------+-------------+------------+-------------+-------------+
| COMPLAINT_TEXT   | TEXT       | NOT NULL    | UNIQUE     |             |             |
+------------------+------------+-------------+------------+-------------+-------------+
| COMPLAINT_OBJECT | TEXT       | NOT NULL    | NOT UNIQUE |             |             |
+------------------+------------+-------------+------------+-------------+-------------+
| CRT_ID           | TIME_STAMP | NOT NULL    | UNIQUE     |             | USERS       |
+------------------+------------+-------------+------------+-------------+-------------+
| IS_DONE          | INTEGER    | NOT NULL    | NOT UNIQUE |             |             |
+------------------+------------+-------------+------------+-------------+-------------+

   + *IS_DONE:* Holds the info whether complaint is evaluated or not.



Comments Table
--------------

+--------------+------------+-------------+------------+-------------+-------------+
| Name         | Data Type  | Null Option | Uniqueness | Primary Key | Foreign Key |
+==============+============+=============+============+=============+=============+
| ID           | SERIAL     | NOT NULL    | NOT UNIQUE | PRIMARY     |             |
+--------------+------------+-------------+------------+-------------+-------------+
| POST_ID      | INTEGER    | NOT NULL    | UNIQUE     |             | POSTS       |
+--------------+------------+-------------+------------+-------------+-------------+
| COMMENT_TEXT | TEXT       | NOT NULL    | NOT UNIQUE |             |             |
+--------------+------------+-------------+------------+-------------+-------------+
| CRT_ID       | INTEGER    | NOT NULL    | UNIQUE     |             | USERS       |
+--------------+------------+-------------+------------+-------------+-------------+
| CRT_TIME     | TIME-STAMP | NOT NULL    | NOT UNIQUE |             |             |
+--------------+------------+-------------+------------+-------------+-------------+
| UPD_ID       | INTEGER    | NULL        | UNIQUE     |             |             |
+--------------+------------+-------------+------------+-------------+-------------+
| UPD_TIME     | TIME-STAMP | NULL        | NOT UNIQUE |             |             |
+--------------+------------+-------------+------------+-------------+-------------+

   + *CRT_ID:* Indicates the user of the users table.
   + *POST_ID:* Holds the id of post referenced from Posts table.


pLikes (Post Likes) Table
-------------------------

+---------+-----------+-------------+------------+-------------+-------------+
| Name    | Data Type | Null Option | Uniqueness | Primary Key | Foreign Key |
+=========+===========+=============+============+=============+=============+
| USER_ID | INTEGER   | NOT NULL    | UNIQUE     | PRIMARY KEY | USERS       |
+---------+-----------+-------------+------------+-------------+-------------+
| POST_ID | INTEGER   | NOT NULL    | UNIQUE     | PRIMARY KEY | POSTS       |
+---------+-----------+-------------+------------+-------------+-------------+

   + *USER_ID:* Indicates the user from users table.







