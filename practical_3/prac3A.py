# Writing to a text file
with open("pds.txt", "w") as file:
    file.write("PDS is a Python for Data Science course.\n")
    file.write("DBMS is another subject.\n")
    file.write("PDS practicals are performed in Python.\n")
    file.write("Data Science is an important field.\n")
    file.write("PDS helps us learn data analysis.\n")

# Reading the text file
with open("pds.txt", "r") as file:
    lines = file.readlines()

print("Contents of file:")
for line in lines:
    print(line, end="")

# Count total lines
total_lines = len(lines)

# Count lines starting with PDS
pds_lines = 0

for line in lines:
    if line.strip().startswith("PDS"):
        pds_lines += 1

print("\n\nTotal number of lines:", total_lines)
print("Number of lines starting with 'PDS':", pds_lines)