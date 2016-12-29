Tags Table
----------

+------+-----------+-------------+------------+-------------+-------------+
| Name | Data Type | Null Option | Uniqueness | Primary Key | Foreign Key |
+======+===========+=============+============+=============+=============+
| ID   | SERIAL    | NOT NULL    | UNIQUE     | PRIMARY KEY |             |
+------+-----------+-------------+------------+-------------+-------------+
| NAME | TEXT      | NOT NULL    | UNIQUE     |             |             |
+------+-----------+-------------+------------+-------------+-------------+


Comment Likes Table
-------------------

+------------+-----------+-------------+------------+-------------+-------------+
| Name       | Data Type | Null Option | Uniqueness | Primary Key | Foreign Key |
+============+===========+=============+============+=============+=============+
| USER_ID    | INTEGER   | NOT NULL    | UNIQUE     | PRIMARY KEY | USERS       |
+------------+-----------+-------------+------------+-------------+-------------+
| COMMENT_ID | INTEGER   | NOT NULL    | UNIQUE     | PRIMARY KEY | COMMENTS    |
+------------+-----------+-------------+------------+-------------+-------------+

   + *USER_ID:* Indicates the user from users table.
   + *COMMENT_ID:* Holds the id of the comment referenced from comments table.


Posts Table
-----------

+-----------+------------+-------------+------------+-------------+-------------+
| Name      | Data Type  | Null Option | Uniqueness | Primary Key | Foreign Key |
+===========+============+=============+============+=============+=============+
| ID        | SERIAL     | NOT NULL    | NOT UNIQUE | PRIMARY     |             |
+-----------+------------+-------------+------------+-------------+-------------+
| TITLE     | TEXT       | NOT NULL    | UNIQUE     |             |             |
+-----------+------------+-------------+------------+-------------+-------------+
| POST_TEXT | TEXT       | NOT NULL    | NOT UNIQUE |             |             |
+-----------+------------+-------------+------------+-------------+-------------+
| TAG_ID    | INTEGER    | NOT NULL    | UNIQUE     |             | TAGS        |
+-----------+------------+-------------+------------+-------------+-------------+
| CRT_ID    | INTEGER    | NOT NULL    | NOT UNIQUE |             | USERS       |
+-----------+------------+-------------+------------+-------------+-------------+
| CRT_TIME  | TIME-STAMP | NULL        | UNIQUE     |             |             |
+-----------+------------+-------------+------------+-------------+-------------+
| UPD_ID    | INTEGER    | NULL        | NOT UNIQUE |             |             |
+-----------+------------+-------------+------------+-------------+-------------+
| UPD_TIME  | TIME-STAMP | NULL        | NOT UNIQUE |             |             |
+-----------+------------+-------------+------------+-------------+-------------+
| GROUP_ID  | INTEGER    | NULL        | NOT UNIQUE |             | GROUPS      |
+-----------+------------+-------------+------------+-------------+-------------+

   + *CRT_ID:* Indicates the user of the users table.
   + *TAG_ID:* Holds the id of tag referenced from tags table.
