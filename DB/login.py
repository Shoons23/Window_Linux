import mysql.connector

DB_SET = {
    "HOST" : "database-ros2.cbqumyg4gbor.ap-northeast-2.rds.amazonaws.com",
    "DATABASE" : "final_ros2",
    "USER" : "dev",
    "PASSWORD" : "0625"
}

remote = mysql.connector.connect(
                host=DB_SET['HOST'],                               
                database=DB_SET['DATABASE'],
                user=DB_SET['USER'],
                password=DB_SET['PASSWORD']
            )

cur = remote.cursor()
cur.execute("SELECT * FROM CAR_INFO")

result = cur.fetchall()
for result_iterator in result:
    print(result_iterator)

remote.close()