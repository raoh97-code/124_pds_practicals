student = {
    "Enrollment No": 124,
    "Name": "Harsh",
    "Branch": "Computer Engineering",
    "Semester": 5,
    "SPI": 8.5
}

print("Student Dictionary:")
print(student)

# Accessing values
print("\nStudent Name:", student["Name"])
print("SPI:", student["SPI"])

# Adding a new item
student["City"] = "Ahmedabad"
print("\nAfter adding City:")
print(student)

# Updating a value
student["SPI"] = 8.7
print("\nAfter updating SPI:")
print(student)

# Deleting an item
del student["City"]
print("\nAfter deleting City:")
print(student)

# Display keys
print("\nKeys:", student.keys())

# Display values
print("Values:", student.values())

# Display key-value pairs
print("Items:", student.items())