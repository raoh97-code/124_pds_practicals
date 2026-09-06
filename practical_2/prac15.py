students = [
    {
        "Enrollment No": 101,
        "Name": "Harsh",
        "Branch": "Computer Engineering",
        "SPI": 9.5
    },
    {
        "Enrollment No": 102,
        "Name": "Rahul",
        "Branch": "Computer Engineering",
        "SPI": 9.2
    },
    {
        "Enrollment No": 103,
        "Name": "Amit",
        "Branch": "IT",
        "SPI": 8.9
    },
    {
        "Enrollment No": 104,
        "Name": "Yash",
        "Branch": "Computer Engineering",
        "SPI": 7.5
    },
    {
        "Enrollment No": 105,
        "Name": "Jay",
        "Branch": "IT",
        "SPI": 7.8
    },
    {
        "Enrollment No": 106,
        "Name": "Raj",
        "Branch": "Computer Engineering",
        "SPI": 9.0
    },
    {
        "Enrollment No": 107,
        "Name": "Dev",
        "Branch": "IT",
        "SPI": 8.2
    }
]

# Sort in descending order of SPI
students.sort(key=lambda student: student["SPI"], reverse=True)

print("TOP 5 STUDENTS :")

for student in students[:5]:
    print("\nEnrollment No:", student["Enrollment No"])
    print("Name:", student["Name"])
    print("Branch:", student["Branch"])
    print("SPI:", student["SPI"])