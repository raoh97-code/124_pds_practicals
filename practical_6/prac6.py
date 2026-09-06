import pandas as pd
import numpy as np
from scipy import stats

# Column names of Adult Census Income Dataset

columns = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
    "income"
]

# Make .csv file of the dataset
df = pd.read_csv('adult.data', sep = ",", header = None, names=columns)
df.to_csv("adult.csv", index=False)


# Read the dataset
data = pd.read_csv(
    "adult.csv",
    na_values="?",
    skipinitialspace=True
)


print("Adult Census Income Dataset")
print("--------------------------------")

print("Number of rows:", data.shape[0])
print("Number of columns:", data.shape[1])


# Select numerical attributes
numeric_data = data.select_dtypes(include=np.number)

print("\nNumerical Attributes:")
print(numeric_data.columns.tolist())


# Descriptive Statistics
print("\nDESCRIPTIVE STATISTICS:")

# Mean
print("\nMean:")
print(numeric_data.mean())


# Median
print("\nMedian:")
print(numeric_data.median())


# Mode
print("\nMode:")

for column in numeric_data.columns:
    mode_value = stats.mode(
        numeric_data[column].dropna(),
        keepdims=True
    ).mode[0]

    print(column, ":", mode_value)


# Variance
print("\nVariance:")
print(numeric_data.var())


# Skewness
print("\nSkewness:")

for column in numeric_data.columns:
    value = stats.skew(
        numeric_data[column].dropna()
    )

    print(column, ":", value)


# Kurtosis
print("\nKurtosis:")

for column in numeric_data.columns:
    value = stats.kurtosis(
        numeric_data[column].dropna()
    )

    print(column, ":", value)
