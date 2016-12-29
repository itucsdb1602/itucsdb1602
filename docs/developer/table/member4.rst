Announcement Table
------------------
+-------------+-------------+-------------+------------+-------------+-------------+
| Name        | Data Type   | Null Option | Uniqueness | Primary Key | Foreign Key |
+=============+=============+=============+============+=============+=============+
| ID          | INT         | NOT NULL    | UNIQUE     | PRIMARY KEY |             |
+-------------+-------------+-------------+------------+-------------+-------------+
| name        | VARCHAR(40) | NOT NULL    | UNIQUE     |             |             |
+-------------+-------------+-------------+------------+-------------+-------------+
| fromuserid  | INT         |             | NOT UNIQUE |             | FOREIGN KEY |
+-------------+-------------+-------------+------------+-------------+-------------+
| fromgroupid | INT         |             | NOT UNIQUE |             | FOREIGN KEY |
+-------------+-------------+-------------+------------+-------------+-------------+
| crt_time    | TIMESTAMP   | NOT NULL    | NOT UNIQUE |             |             |
+-------------+-------------+-------------+------------+-------------+-------------+

   + *ID:* Holds the id of announcement referenced from Announcement table.
   + *name:* Holds the name of announcement referenced from Announcement table.
   + *fromuserid:* Indicates the which user create the Announcement. Referenced from User table.
   + *fromgroupid:* Indicates the which group create the Announcement. Referenced from Group table.
   + *crt_time:* Holds the time of creat time of announcement.

Group Table
-----------

+------+-------------+-------------+------------+-------------+-------------+
| Name | Data Type   | Null Option | Uniqueness | Primary Key | Foreign Key |
+======+=============+=============+============+=============+=============+
| ID   | INTEGER     | NOT NULL    | UNIQUE     | PRIMARY KEY |             |
+------+-------------+-------------+------------+-------------+-------------+
| name | VARCHAR(40) | NOT NULL    | NOT UNIQUE |             |             |
+------+-------------+-------------+------------+-------------+-------------+


   + *id:* Holds the id of group referenced from Group table.
   + *name:* Holds the name of group referenced from Group table.

Group-User Table
----------------

+----------+-----------+-------------+------------+-------------+-------------+
| Name     | Data Type | Null Option | Uniqueness | Primary Key | Foreign Key |
+==========+===========+=============+============+=============+=============+
| USER_ID  | INTEGER   | NOT NULL    | UNIQUE     | PRIMARY KEY | FOREIGN KEY |
+----------+-----------+-------------+------------+-------------+-------------+
| GROUP_ID | INTEGER   | NOT NULL    | UNIQUE     | PRIMARY KEY | FOREIGN KEY |
+----------+-----------+-------------+------------+-------------+-------------+
| IS_ADMIN | INTEGER   |             |            |             | FOREIGN KEY |
+----------+-----------+-------------+------------+-------------+-------------+

   + *USER_ID:* Indicates the name of the which user in group. Referenced User table.
   + *GROUP_ID:* Holds the id of the group referenced from Group table.
   + *IS_ADMIN:* Holds the admin knowledge of the user. Referenced User table.
