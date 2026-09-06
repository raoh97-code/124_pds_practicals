import pickle

student = {
    "Enrollment No": 101,
    "Name": "Harsh",
    "Branch": "Computer Engineering",
    "SPI": 8.5
}

# Writing binary file
with open("student.dat", "wb") as file:
    pickle.dump(student, file)

print("\nBinary file written successfully.")

# Reading binary file
with open("student.dat", "rb") as file:
    data = pickle.load(file)

print("\nData read from binary file:")
print(data)