numbers = list(map(int, input("Enter list elements separated by spaces: ").split()))

element = int(input("Enter element to find: "))

count = numbers.count(element)

print("List:", numbers)
print("Occurrence of", element, "=", count)

if count > 0:
    print("Element found in the list.")
else:
    print("Element not found in the list.")