import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    mean_squared_error,
    r2_score
)


# Read the dataset

data = pd.read_csv("diabetes.csv")

print("Pima Indians Diabetes Dataset")
print("--------------------------------")

print("Number of rows:", data.shape[0])
print("Number of columns:", data.shape[1])

print("\nFirst five records:")
print(data.head())


# CLASSIFICATION
# Predict Outcome
print("\nCLASSIFICATION:")


# Independent variables
X = data.drop("Outcome", axis=1)

# Target variable
y = data["Outcome"]


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Standardize the features
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Create Logistic Regression model
classification_model = LogisticRegression(
    max_iter=1000
)


# Train the model
classification_model.fit(
    X_train_scaled,
    y_train
)


# Make predictions
y_pred = classification_model.predict(
    X_test_scaled
)


# Calculate accuracy
accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\nClassification Accuracy:")
print(accuracy)


# Confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))



# REGRESSION
# Predict Glucose

print("\nREGRESSION:")


# Glucose will be the continuous target
X_reg = data.drop(
    ["Glucose", "Outcome"],
    axis=1
)

y_reg = data["Glucose"]


# Split data
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg,
    y_reg,
    test_size=0.2,
    random_state=42
)


# Create Linear Regression model
regression_model = LinearRegression()


# Train the model
regression_model.fit(
    X_train_reg,
    y_train_reg
)


# Make predictions
y_pred_reg = regression_model.predict(
    X_test_reg
)


# Calculate Mean Squared Error
mse = mean_squared_error(
    y_test_reg,
    y_pred_reg
)


# Calculate R2 score
r2 = r2_score(
    y_test_reg,
    y_pred_reg
)


print("\nMean Squared Error:")
print(mse)

print("\nR2 Score:")
print(r2)


# Display some actual and predicted values
print("\nActual vs Predicted Glucose:")

for actual, predicted in zip(
    y_test_reg.iloc[:10],
    y_pred_reg[:10]
):
    print(
        "Actual:",
        actual,
        " Predicted:",
        round(predicted, 2)
    )