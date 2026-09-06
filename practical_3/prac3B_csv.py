import csv

students = [
    [101, "Harsh", "Computer Engineering", 8.5],
    [102, "Rahul", "Computer Engineering", 9.2],
    [103, "Amit", "IT", 8.9]
]

# Writing CSV file
with open("students.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Enrollment No", "Name", "Branch", "SPI"])
    writer.writerows(students)

print("CSV file written successfully.")

# Reading CSV file
print("\nCSV file contents:")

with open("students.csv", "r") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)