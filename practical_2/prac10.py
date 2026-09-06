# List containing [name, marks]
students = [
    ["Harsh", 82],
    ["Rahul", 75],
    ["Amit", 91],
    ["Yash", 68],
    ["Jay", 88]
]

# Sort according to marks using lambda
students.sort(key=lambda x: x[1])

print("Sorted list according to marks:")
for student in students:
    print(student)

marks = [student[1] for student in students]

print("\nSmallest number:", min(marks))
print("Largest number:", max(marks))
print("Sum of all members:", sum(marks))