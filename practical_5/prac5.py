import pandas as pd

# Creating a Pandas Series
marks = pd.Series([85, 78, 92, 67, 88])
print("Pandas Series:")
print(marks)

# Creating a Pandas DataFrame
students = {
    "Enrollment_No": [101, 102, 103, 104, 105],
    "Name": ["Harsh", "Rahul", "Amit", "Om", "Jay"],
    "Branch": ["CE", "CE", "IT", "CE", "IT"],
    "Semester": [5, 5, 5, 5, 5],
    "SPI": [8.5, 9.2, 8.9, 7.8, 9.0]
}
df = pd.DataFrame(students)
print("\nPandas DataFrame:")
print(df)

# Writing DataFrame to CSV file
df.to_csv("students.csv", index=False)
print("\nDataset saved as students.csv")

# Reading Dataset
data = pd.read_csv("students.csv")
print("\nDataset:")
print(data)

# head() - First five records
print("\nFirst five records:")
print(data.head())

# tail() - Last five records
print("\nLast five records:")
print(data.tail())

# info() - Information about dataset
print("\nInformation about dataset:")
data.info()

# describe() - Statistical summary
print("\nStatistical description:")
print(data.describe())

# Indexing
print("\nValue at row 2, column Name:")
print(data.loc[2, "Name"])

# Selecting a column
print("\nName column:")
print(data["Name"])

# Selecting multiple columns
print("\nName and SPI columns:")
print(data[["Name", "SPI"]])

# Selecting rows using iloc
print("\nFirst three rows:")
print(data.iloc[:3])

# Selecting students with SPI greater than 8.5
print("\nStudents with SPI greater than 8.5:")
print(data[data["SPI"] > 8.5])