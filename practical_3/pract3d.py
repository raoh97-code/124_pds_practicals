import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="password")
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS academic_db")
cursor.execute("USE academic_db")
cursor.execute("CREATE TABLE IF NOT EXISTS Student_Records (ID VARCHAR(10) PRIMARY KEY, Name
VARCHAR(50), GPA FLOAT)")
cursor.execute("INSERT INTO Student_Records VALUES (%s, %s, %s)", ("001", "Karan Patel", 8.75))
cursor.execute("UPDATE Student_Records SET GPA = %s WHERE ID = %s", (9.00, "001"))
conn.commit()
cursor.execute("SELECT * FROM Student_Records WHERE GPA >= %s", (8.5,))
print("Filtered Records:", cursor.fetchall())
conn.close()