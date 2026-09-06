import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harshrao@1403",
    port=3306
)

cursor = connection.cursor(buffered=True)
cursor.execute("CREATE DATABASE IF NOT EXISTS pds_student_db")
cursor.execute("USE pds_student_db")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    Enrollment_No INT PRIMARY KEY,
    Name VARCHAR(100),
    Branch VARCHAR(100),
    Semester INT,
    SPI FLOAT
)
""")
connection.commit()
def insert_student():
    enrollment = int(input("Enter Enrollment No: "))
    name = input("Enter Name: ")
    branch = input("Enter Branch: ")
    semester = int(input("Enter Semester: "))
    spi = float(input("Enter SPI: "))

    query = """
    INSERT INTO Students
    (Enrollment_No, Name, Branch, Semester, SPI)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (enrollment, name, branch, semester, spi)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Student inserted successfully.")

    except mysql.connector.Error as e:
        print("Error:", e)

def display_students():
    cursor.execute("SELECT * FROM Students")

    records = cursor.fetchall()

    if not records:
        print("No student records found.")
        return

    for record in records:
        print(record)

def update_student():
    enrollment = int(input("Enter Enrollment No to update: "))

    name = input("Enter new Name: ")
    branch = input("Enter new Branch: ")
    semester = int(input("Enter new Semester: "))
    spi = float(input("Enter new SPI: "))

    query = """
    UPDATE Students
    SET Name = %s,
        Branch = %s,
        Semester = %s,
        SPI = %s
    WHERE Enrollment_No = %s
    """

    values = (name, branch, semester, spi, enrollment)

    cursor.execute(query, values)
    connection.commit()

    if cursor.rowcount > 0:
        print("Student updated successfully.")
    else:
        print("Student not found.")

def delete_student():
    enrollment = int(input("Enter Enrollment No to delete: "))

    query = "DELETE FROM Students WHERE Enrollment_No = %s"

    cursor.execute(query, (enrollment,))
    connection.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully.")
    else:
        print("Student not found.")

def search_student():
    enrollment = int(input("Enter Enrollment No to search: "))

    query = "SELECT * FROM Students WHERE Enrollment_No = %s"

    cursor.execute(query, (enrollment,))

    record = cursor.fetchone()

    if record:
        print("Student found:")
        print(record)
    else:
        print("Student not found.")

def filter_by_spi():
    threshold = float(input("Enter SPI threshold: "))

    query = "SELECT * FROM Students WHERE SPI >= %s"

    cursor.execute(query, (threshold,))

    records = cursor.fetchall()

    if records:
        print("\nStudents with SPI >=", threshold)

        for record in records:
            print(record)
    else:
        print("No students found.")

while True:

    print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
    print("1. Insert Student")
    print("2. Display Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Search Student")
    print("6. Filter by SPI")
    print("7. Exit")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            insert_student()

        elif choice == 2:
            display_students()

        elif choice == 3:
            update_student()

        elif choice == 4:
            delete_student()

        elif choice == 5:
            search_student()

        elif choice == 6:
            filter_by_spi()

        elif choice == 7:
            print("Program exited.")
            break

        else:
            print("Invalid choice.")

    except ValueError:
        print("Please enter a valid number.")

    except mysql.connector.Error as e:
        print("Database error:", e)

cursor.close()
connection.close()