from pathlib import Path
import zipfile, textwrap

base = Path("/mnt/data/PDS_Practicals_1_2_3")
base.mkdir(exist_ok=True)

files = {
"Pract_1/01_strings.py": r'''s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

print("String 1:", s1)
print("String 2:", s2)
print("Concatenation:", s1 + s2)
print("Length:", len(s1), len(s2))
print("Uppercase:", s1.upper(), s2.upper())
print("Lowercase:", s1.lower(), s2.lower())
print("First character:", s1[0] if s1 else "Empty")
print("Last character:", s2[-1] if s2 else "Empty")
print("s1 == s2:", s1 == s2)
print("s1 in s2:", s1 in s2)
print("Reversed:", s1[::-1], s2[::-1])
''',

"Pract_1/02_dob_age_calendar.py": r'''from datetime import date, datetime
import calendar

def validate_dob(value):
    try:
        dob = datetime.strptime(value, "%Y-%m-%d").date()
        if dob > date.today():
            return None
        return dob
    except ValueError:
        return None

name = input("Enter name: ")
dob_text = input("Enter date of birth (YYYY-MM-DD): ")
dob = validate_dob(dob_text)

if dob is None:
    print("Invalid date of birth.")
else:
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    turns_100 = dob.year + 100

    print(f"\nName: {name}")
    print(f"Current age: {age}")
    print(f"Year {name} turns 100: {turns_100}")
    print(f"\nCalendar for {dob.strftime('%B')} {dob.year}:")
    print(calendar.month(dob.year, dob.month))
''',

"Pract_1/03_odd_even_extremes.py": r'''numbers = []

for i in range(10):
    while True:
        try:
            numbers.append(int(input(f"Enter number {i + 1}: ")))
            break
        except ValueError:
            print("Please enter an integer.")

odd = [x for x in numbers if x % 2 != 0]
even = [x for x in numbers if x % 2 == 0]

print("\nNumbers:", numbers)
print("Odd count:", len(odd))
print("Even count:", len(even))

if odd:
    print("Smallest odd:", min(odd))
    print("Largest odd:", max(odd))
else:
    print("No odd numbers.")

if even:
    print("Smallest even:", min(even))
    print("Largest even:", max(even))
else:
    print("No even numbers.")
''',

"Pract_1/04_menu_calculator.py": r'''import math

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid numeric input.")

while True:
    print("""
--- Calculator ---
1. Addition
2. Subtraction
3. Multiplication
4. Division
5. Square root
6. Power
7. Modulus
8. Exit
""")
    choice = input("Enter choice: ").strip()

    try:
        if choice == "8":
            print("Exiting calculator.")
            break
        elif choice in {"1", "2", "3", "4", "6", "7"}:
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")

            if choice == "1":
                print("Result:", a + b)
            elif choice == "2":
                print("Result:", a - b)
            elif choice == "3":
                print("Result:", a * b)
            elif choice == "4":
                if b == 0:
                    raise ZeroDivisionError("Cannot divide by zero.")
                print("Result:", a / b)
            elif choice == "6":
                print("Result:", a ** b)
            elif choice == "7":
                if b == 0:
                    raise ZeroDivisionError("Cannot take modulus by zero.")
                print("Result:", a % b)
        elif choice == "5":
            a = get_number("Enter number: ")
            if a < 0:
                raise ValueError("Square root of a negative number is not real.")
            print("Result:", math.sqrt(a))
        else:
            print("Invalid menu choice.")
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        print("Error:", e)
''',

"Pract_1/05_armstrong.py": r'''def is_armstrong(n):
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    return sum(int(d) ** power for d in digits) == n

n = int(input("Enter an integer: "))

# With user-defined function
print("Using function:", "Armstrong number" if is_armstrong(n) else "Not an Armstrong number")

# Without user-defined function
if n >= 0:
    digits = str(n)
    power = len(digits)
    total = sum(int(d) ** power for d in digits)
    print("Without function:", "Armstrong number" if total == n else "Not an Armstrong number")
else:
    print("Without function: Not an Armstrong number")
''',

"Pract_1/06_pascals_triangle.py": r'''def pascal(n):
    row = [1]
    for _ in range(n):
        print(" ".join(map(str, row)))
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]

n = int(input("Enter number of rows: "))
if n < 0:
    print("Number of rows cannot be negative.")
else:
    pascal(n)
''',

"Pract_1/07_pangram.py": r'''def is_pangram(text):
    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    return alphabet.issubset(set(text.lower()))

text = input("Enter a string: ")
print("Pangram" if is_pangram(text) else "Not a pangram")
''',

"Pract_1/08_hcf_gcd.py": r'''def hcf(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("HCF/GCD:", hcf(a, b))
''',

"Pract_2/09_list_occurrence.py": r'''items = input("Enter list elements separated by spaces: ").split()
target = input("Enter element to search: ")

count = items.count(target)
print("Occurrence:", count)

if count:
    print("Positions:", [i for i, value in enumerate(items) if value == target])
else:
    print("Element not found.")
''',

"Pract_2/10_sort_lambda.py": r'''# A list of lists is used so that sorting "according to a column" is demonstrated.
data = [
    [101, 72, "A"],
    [102, 91, "B"],
    [103, 65, "A"],
    [104, 84, "C"],
    [105, 78, "B"]
]

column = int(input("Enter column index to sort by (0, 1, or 2): "))

if column not in range(3):
    print("Invalid column.")
else:
    sorted_data = sorted(data, key=lambda row: row[column])
    print("Sorted list:")
    for row in sorted_data:
        print(row)

    numbers = [row[1] for row in data]
    print("Smallest number:", min(numbers))
    print("Largest number:", max(numbers))
    print("Sum:", sum(numbers))
''',

"Pract_2/11_marks_tuple.py": r'''marks = tuple(map(float, input("Enter students' PDS marks separated by spaces: ").split()))

print("Marks tuple:", marks)
print("Number of students:", len(marks))
''',

"Pract_2/12_set_operations.py": r'''enrolments = set(input("Enter enrolment numbers separated by spaces: ").split())

print("Original set:", enrolments)
print("Sorted set:", sorted(enrolments))

new_id = input("Enter enrolment number to add: ")
enrolments.add(new_id)
print("After add:", enrolments)

delete_id = input("Enter enrolment number to delete: ")
enrolments.discard(delete_id)
print("After delete:", enrolments)

other = set(input("Enter another set of enrolment numbers: ").split())
print("Other set:", other)
print("Union:", enrolments | other)
print("Intersection:", enrolments & other)
print("Difference (first - second):", enrolments - other)
print("Symmetric difference:", enrolments ^ other)

test_id = input("Enter enrolment number to test membership: ")
print("Membership:", test_id in enrolments)
''',

"Pract_2/13_student_dictionary.py": r'''student = {
    "enrollment_no": input("Enrollment No: "),
    "name": input("Name: "),
    "branch": input("Branch: "),
    "semester": int(input("Semester: ")),
    "spi": float(input("SPI: "))
}

print("\nDictionary:", student)
print("Keys:", student.keys())
print("Values:", student.values())
print("Items:", student.items())

key = input("Enter a key to retrieve: ")
print("Value:", student.get(key, "Key not found"))

new_name = input("Enter updated name: ")
student["name"] = new_name

student["status"] = "Active"
print("After update/add:", student)

removed = student.pop("status", None)
print("Removed value:", removed)
print("Final dictionary:", student)
''',

"Pract_2/14_character_count_dictionary.py": r'''text = input("Enter a string: ")

char_count = {}
for ch in text:
    char_count[ch] = char_count.get(ch, 0) + 1

print("Character-count dictionary:")
print(char_count)
''',

"Pract_2/15_top5_students.py": r'''students = [
    {"enrollment_no": "E101", "name": "Aarav", "branch": "CE", "spi": 9.21},
    {"enrollment_no": "E102", "name": "Bhavya", "branch": "CE", "spi": 8.74},
    {"enrollment_no": "E103", "name": "Chirag", "branch": "IT", "spi": 9.65},
    {"enrollment_no": "E104", "name": "Diya", "branch": "CE", "spi": 8.92},
    {"enrollment_no": "E105", "name": "Esha", "branch": "IT", "spi": 9.44},
    {"enrollment_no": "E106", "name": "Farhan", "branch": "CE", "spi": 8.51},
    {"enrollment_no": "E107", "name": "Gauri", "branch": "IT", "spi": 9.08}
]

students.sort(key=lambda s: s["spi"], reverse=True)

print("Top 5 students:")
for rank, student in enumerate(students[:5], start=1):
    print(rank, student)
''',

"Pract_3/a_text_file.py": r'''filename = "pds_text.txt"

content = """PDS is a Python for Data Science course.
Python is useful for data analysis.
PDS practicals include file handling.
PDS also introduces data structures.
This line does not start with the required prefix.
"""

with open(filename, "w", encoding="utf-8") as file:
    file.write(content)

with open(filename, "r", encoding="utf-8") as file:
    lines = file.readlines()

total_lines = len(lines)
pds_lines = sum(1 for line in lines if line.startswith("PDS"))

print("File contents:")
print("".join(lines))
print("Total lines:", total_lines)
print("Lines starting with 'PDS':", pds_lines)
''',

"Pract_3/b_csv_binary.py": r'''import csv
import pickle

# CSV write
rows = [
    ["Enrollment No", "Name", "Branch", "SPI"],
    ["E101", "Aarav", "CE", 9.21],
    ["E102", "Bhavya", "CE", 8.74],
    ["E103", "Chirag", "IT", 9.65]
]

with open("students.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(rows)

# CSV read
print("CSV contents:")
with open("students.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Binary write/read using pickle
student_data = {
    "E101": {"name": "Aarav", "branch": "CE", "spi": 9.21},
    "E102": {"name": "Bhavya", "branch": "CE", "spi": 8.74}
}

with open("students.dat", "wb") as file:
    pickle.dump(student_data, file)

with open("students.dat", "rb") as file:
    loaded_data = pickle.load(file)

print("\nBinary data read back:")
print(loaded_data)
''',

"Pract_3/c_exception_handling.py": r'''class InvalidSPIError(Exception):
    """User-defined exception for an invalid SPI."""
    pass

def validate_spi(spi):
    if not 0 <= spi <= 10:
        raise InvalidSPIError("SPI must be between 0 and 10.")
    return True

try:
    a = int(input("Enter an integer: "))
    b = int(input("Enter another integer: "))
    print("Division:", a / b)

    spi = float(input("Enter SPI: "))
    validate_spi(spi)
    print("Valid SPI:", spi)

except ValueError:
    print("Built-in exception: invalid numeric input.")
except ZeroDivisionError:
    print("Built-in exception: division by zero.")
except InvalidSPIError as e:
    print("User-defined exception:", e)
finally:
    print("Exception handling demonstration complete.")
''',

"Pract_3/d_student_management_mysql.py": r'''# Requires:
#   pip install mysql-connector-python
#
# Before running, set MYSQL_PASSWORD below (and MYSQL_HOST/USER if needed).

import mysql.connector
from mysql.connector import Error

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "YOUR_PASSWORD"
DB_NAME = "pds_student_db"

def connect(server=True):
    config = {
        "host": MYSQL_HOST,
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD
    }
    if not server:
        config["database"] = DB_NAME
    return mysql.connector.connect(**config)

def setup_database():
    conn = connect(server=True)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cur.close()
    conn.close()

    conn = connect(server=False)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            Enrollment_No VARCHAR(30) PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Branch VARCHAR(50) NOT NULL,
            Semester INT NOT NULL,
            SPI DECIMAL(4,2) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_student():
    data = (
        input("Enrollment No: "),
        input("Name: "),
        input("Branch: "),
        int(input("Semester: ")),
        float(input("SPI: "))
    )
    conn = connect(False)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Students
            (Enrollment_No, Name, Branch, Semester, SPI)
            VALUES (%s, %s, %s, %s, %s)
        """, data)
        conn.commit()
        print("Student inserted.")
    except Error as e:
        print("Insert error:", e)
    finally:
        cur.close()
        conn.close()

def update_student():
    enrollment = input("Enrollment No to update: ")
    print("1. Name  2. Branch  3. Semester  4. SPI")
    choice = input("Choose field: ")

    fields = {"1": "Name", "2": "Branch", "3": "Semester", "4": "SPI"}
    if choice not in fields:
        print("Invalid choice.")
        return

    new_value = input("New value: ")
    if choice == "3":
        new_value = int(new_value)
    elif choice == "4":
        new_value = float(new_value)

    conn = connect(False)
    cur = conn.cursor()
    cur.execute(f"UPDATE Students SET {fields[choice]} = %s WHERE Enrollment_No = %s",
                (new_value, enrollment))
    conn.commit()
    print("Rows updated:", cur.rowcount)
    cur.close()
    conn.close()

def delete_student():
    enrollment = input("Enrollment No to delete: ")
    conn = connect(False)
    cur = conn.cursor()
    cur.execute("DELETE FROM Students WHERE Enrollment_No = %s", (enrollment,))
    conn.commit()
    print("Rows deleted:", cur.rowcount)
    cur.close()
    conn.close()

def search_students():
    enrollment = input("Enrollment No (press Enter to filter by SPI): ").strip()
    conn = connect(False)
    cur = conn.cursor(dictionary=True)

    if enrollment:
        cur.execute("SELECT * FROM Students WHERE Enrollment_No = %s", (enrollment,))
    else:
        threshold = float(input("Show students with SPI >= "))
        cur.execute("SELECT * FROM Students WHERE SPI >= %s ORDER BY SPI DESC", (threshold,))

    rows = cur.fetchall()
    if not rows:
        print("No records found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def main():
    try:
        setup_database()
        while True:
            print("""
--- Student Management System ---
1. Insert
2. Update
3. Delete
4. Search / SPI filter
5. Exit
""")
            choice = input("Enter choice: ")
            if choice == "1":
                insert_student()
            elif choice == "2":
                update_student()
            elif choice == "3":
                delete_student()
            elif choice == "4":
                search_students()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")
    except Error as e:
        print("MySQL error:", e)

if __name__ == "__main__":
    main()
'''
}

for rel, content in files.items():
    path = base / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

readme = """# PDS Practicals 1, 2 and 3

Based on the uploaded GTU/L.D. College of Engineering practical list.

## Contents
- Pract-1: Programs 1–8
- Pract-2: Programs 9–15
- Pract-3: Text files, CSV/binary files, exception handling, and Python–MySQL Student Management System

## Running
Python 3.10+ is recommended.

For the MySQL practical:
1. Install MySQL Server.
2. Install connector: `pip install mysql-connector-python`
3. Open `Pract_3/d_student_management_mysql.py`.
4. Replace `YOUR_PASSWORD` with your MySQL password.
5. Run the file.

The MySQL program creates the `pds_student_db` database and `Students` table automatically.
"""
(base / "README.md").write_text(readme, encoding="utf-8")

zip_path = Path("/mnt/data/PDS_Practicals_1_2_3_Solutions.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in base.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(base.parent))

print(f"Created {len(files)} Python practical solution files.")
print(f"ZIP: {zip_path}")
