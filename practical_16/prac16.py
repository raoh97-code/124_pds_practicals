import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# ------------------------------------------------------------ LOAD + WRANGLE
# single shared dataset: <project>/data/gujarat_companies.csv
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "gujarat_companies.csv"
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.upper()
df = df.drop_duplicates().reset_index(drop=True)

print("=== 1. DATA WRANGLING ===")
# type conversion
df["DATE_OF_REGISTRATION"] = pd.to_datetime(df["DATE_OF_REGISTRATION"],
                                            format="%d-%m-%Y", errors="coerce")
df["REG_YEAR"] = df["DATE_OF_REGISTRATION"].dt.year
df["COMPANY_AGE"] = 2026 - df["REG_YEAR"]

# text cleaning
for col in ["COMPANY_NAME", "COMPANY_STATUS", "COMPANY_CLASS",
            "PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN"]:
    df[col] = df[col].astype(str).str.strip()
df["COMPANY_NAME"] = df["COMPANY_NAME"].str.title()

# missing values
print("Missing values before:\n", df[["AUTHORIZED_CAP", "PAIDUP_CAPITAL",
                                      "COMPANY_SUB_CATEGORY"]].isna().sum())
df["AUTHORIZED_CAP"] = df["AUTHORIZED_CAP"].fillna(df["AUTHORIZED_CAP"].median())
# paid-up capital: fill with median paid-up ratio * authorized capital
ratio = (df["PAIDUP_CAPITAL"] / df["AUTHORIZED_CAP"]).median()
df["PAIDUP_CAPITAL"] = df["PAIDUP_CAPITAL"].fillna(df["AUTHORIZED_CAP"] * ratio)
df["COMPANY_SUB_CATEGORY"] = df["COMPANY_SUB_CATEGORY"].fillna(
    df["COMPANY_SUB_CATEGORY"].mode()[0])
print("\nMissing values after:\n", df[["AUTHORIZED_CAP", "PAIDUP_CAPITAL",
                                       "COMPANY_SUB_CATEGORY"]].isna().sum())

# derived variable and binning
df["PAIDUP_RATIO"] = df["PAIDUP_CAPITAL"] / df["AUTHORIZED_CAP"]
df["CAPITAL_GROUP"] = pd.cut(df["AUTHORIZED_CAP"],
                             [0, 1e6, 1e7, 1e8, np.inf],
                             labels=["Small", "Medium", "Large", "Very Large"])
print("\nCapital group counts:\n", df["CAPITAL_GROUP"].value_counts())

# ---------------------------------------------------------------- OUTLIERS
print("\n=== 2. OUTLIER DETECTION ===")
num_cols = ["AUTHORIZED_CAP", "PAIDUP_CAPITAL"]
for col in num_cols:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_iqr = ((df[col] < low) | (df[col] > high)).sum()
    z = np.abs(stats.zscore(df[col]))
    n_z = (z > 3).sum()
    print(f"{col}: IQR bounds = ({low:,.0f}, {high:,.0f}) -> {n_iqr} outliers | "
          f"Z-score > 3 -> {n_z} outliers")

# boxplot before treatment
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for a, col in zip(ax, num_cols):
    a.boxplot(df[col].dropna())
    a.set_yscale("log")
    a.set_title(f"{col} (before treatment, log scale)")
plt.tight_layout()
plt.savefig("outliers_boxplot.png", dpi=150)
plt.close()

print("\n=== 3. OUTLIER HANDLING ===")
clean = df.copy()
# Method A: removal using IQR
q1, q3 = df["AUTHORIZED_CAP"].quantile([0.25, 0.75])
iqr = q3 - q1
mask = df["AUTHORIZED_CAP"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
print(f"Method A (removal): rows {len(df)} -> {mask.sum()}")

# Method B: capping / winsorizing at 1st and 99th percentile
for col in num_cols:
    lo, hi = df[col].quantile([0.01, 0.99])
    clean[col + "_CAPPED"] = df[col].clip(lo, hi)
    print(f"Method B (capping) {col}: max {df[col].max():,.0f} -> "
          f"{clean[col + '_CAPPED'].max():,.0f}")

# Method C: log transformation (reduces skewness)
for col in num_cols:
    clean[col + "_LOG"] = np.log1p(df[col])
    print(f"Method C (log) {col}: skew {df[col].skew():.2f} -> "
          f"{clean[col + '_LOG'].skew():.2f}")

# ------------------------------------------------------------- NORMALIZATION
print("\n=== 4. NORMALIZATION / STANDARDIZATION ===")
x = clean["AUTHORIZED_CAP_CAPPED"]

# Manual formulas
clean["AUTH_MINMAX_MANUAL"] = (x - x.min()) / (x.max() - x.min())
clean["AUTH_ZSCORE_MANUAL"] = (x - x.mean()) / x.std(ddof=0)

# scikit-learn scalers
clean["AUTH_MINMAX"] = MinMaxScaler().fit_transform(x.to_frame())
clean["AUTH_STANDARD"] = StandardScaler().fit_transform(x.to_frame())
clean["AUTH_ROBUST"] = RobustScaler().fit_transform(x.to_frame())

# Decimal scaling
j = len(str(int(x.abs().max())))
clean["AUTH_DECIMAL"] = x / (10 ** j)

summary = clean[["AUTH_MINMAX", "AUTH_STANDARD", "AUTH_ROBUST", "AUTH_DECIMAL"]].agg(
    ["min", "max", "mean", "std"]).round(4)
print(summary)
print("\nManual and sklearn Min-Max identical:",
      np.allclose(clean["AUTH_MINMAX"], clean["AUTH_MINMAX_MANUAL"]))
print("Manual and sklearn Z-score identical :",
      np.allclose(clean["AUTH_STANDARD"], clean["AUTH_ZSCORE_MANUAL"]))

# comparison plot
fig, ax = plt.subplots(1, 4, figsize=(15, 3.5))
for a, (col, title) in zip(ax, [("AUTHORIZED_CAP_CAPPED", "Capped (original scale)"),
                                ("AUTH_MINMAX", "Min-Max [0,1]"),
                                ("AUTH_STANDARD", "Z-score"),
                                ("AUTH_ROBUST", "Robust")]):
    a.hist(clean[col], bins=40, color="steelblue")
    a.set_title(title)
plt.tight_layout()
plt.savefig("normalization_compare.png", dpi=150)
plt.close()

clean.to_csv("gujarat_companies_wrangled.csv", index=False)
print("\nSaved: gujarat_companies_wrangled.csv, outliers_boxplot.png, "
      "normalization_compare.png")
