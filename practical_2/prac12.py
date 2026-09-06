# Create sets
students_a = {101, 102, 103, 104, 105}
students_b = {104, 105, 106, 107, 108}

print("Set A:", students_a)
print("Set B:", students_b)

# Sort set
print("\nSorted Set A:", sorted(students_a))

# Add
students_a.add(109)
print("\nAfter adding 109:", students_a)

# Delete
students_a.remove(109)
print("After deleting 109:", students_a)

# Union
print("\nUnion:", students_a.union(students_b))

# Intersection
print("Intersection:", students_a.intersection(students_b))

# Difference
print("A - B:", students_a.difference(students_b))

# Symmetric Difference
print("Symmetric Difference:",
      students_a.symmetric_difference(students_b))

# Membership testing
enrollment = int(input("\nEnter enrolment number to search: "))

if enrollment in students_a:
    print(enrollment, "is present in Set A.")
else:
    print(enrollment, "is not present in Set A.")