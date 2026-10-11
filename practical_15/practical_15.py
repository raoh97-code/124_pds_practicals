
from pathlib import Path
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# ---------------------------------------------------------------- 1. LOADING
# single shared dataset: <project>/data/gujarat_companies.csv
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "gujarat_companies.csv"
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.upper()
print("=== 1. DATA LOADING ===")
print("Shape :", df.shape)
print(df.head(), "\n")
df.info()

# ------------------------------------------------------- 2. REMOVE DUPLICATES
print("\n=== 2. REMOVAL OF DUPLICATES ===")
print("Duplicate rows before :", df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)
print("Duplicate rows after  :", df.duplicated().sum())
print("Shape after removal   :", df.shape)

# ------------------------------------------------------ 3. SLICING AND DICING
print("\n=== 3. SLICING AND DICING ===")
print("First 5 rows, first 4 columns (iloc):")
print(df.iloc[:5, :4])
print("\nRows 10-14, selected columns (loc):")
print(df.loc[10:14, ["COMPANY_NAME", "COMPANY_STATUS", "AUTHORIZED_CAP"]])
print("\nEvery 1000th record (step slicing):")
print(df.iloc[::1000, [1, 2, 3]])

# ------------------------------------------------ 4. FILTERING AND SELECTING
print("\n=== 4. FILTERING AND SELECTING ===")
active = df[df["COMPANY_STATUS"] == "Active"]
print("Active companies:", len(active))

big_public = df[(df["COMPANY_CLASS"] == "Public") & (df["AUTHORIZED_CAP"] > 10_000_000)]
print("Public companies with authorized capital > 1 crore:", len(big_public))

selected = df[df["PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN"].isin(["Finance", "Insurance"])]
print("Finance or Insurance companies:", len(selected))

print("Companies with 'Textiles' in name:",
      df["COMPANY_NAME"].str.contains("Textiles", case=False).sum())
print("\nSelected columns only:")
print(df[["COMPANY_NAME", "COMPANY_CLASS", "AUTHORIZED_CAP"]].head())

# --------------------------------------------- 5. CONCATENATING AND TRANSFORMING
print("\n=== 5. CONCATENATING AND TRANSFORMING ===")
# (a) concatenate rows: stack two subsets back together
private_df = df[df["COMPANY_CLASS"] == "Private"].head(3)
public_df = df[df["COMPANY_CLASS"] == "Public"].head(3)
stacked = pd.concat([private_df, public_df], axis=0, ignore_index=True)
print("Row-wise concat (private + public):")
print(stacked[["COMPANY_NAME", "COMPANY_CLASS"]])

# (b) concatenate columns: join a lookup table on a key
roc_info = pd.DataFrame({
    "REGISTRAR_OF_COMPANIES": ["RoC-Ahmedabad", "RoC-Gandhinagar", "RoC-Vadodara",
                               "RoC-Surat", "RoC-Rajkot"],
    "ZONE": ["Central", "Capital", "East", "South", "Saurashtra"]})
df = df.merge(roc_info, on="REGISTRAR_OF_COMPANIES", how="left")
print("\nColumn-wise merge (added ZONE):")
print(df[["REGISTRAR_OF_COMPANIES", "ZONE"]].drop_duplicates())

# (c) transformations
df["DATE_OF_REGISTRATION"] = pd.to_datetime(df["DATE_OF_REGISTRATION"],
                                            format="%d-%m-%Y", errors="coerce")
df["REG_YEAR"] = df["DATE_OF_REGISTRATION"].dt.year
df["COMPANY_NAME"] = df["COMPANY_NAME"].str.strip().str.title()
df["AUTH_CAP_LAKHS"] = df["AUTHORIZED_CAP"] / 1e5
df["COMPANY_STATUS"] = df["COMPANY_STATUS"].astype("category")
print("\nTransformed columns (REG_YEAR, AUTH_CAP_LAKHS):")
print(df[["DATE_OF_REGISTRATION", "REG_YEAR", "AUTHORIZED_CAP", "AUTH_CAP_LAKHS"]].head())

# ------------------------------------- 6. ADDING AND REMOVING CASES/VARIABLES
print("\n=== 6. ADDING AND REMOVING CASES / VARIABLES ===")
# add variable
df["COMPANY_AGE"] = 2026 - df["REG_YEAR"]
df["CAPITAL_SIZE"] = pd.cut(df["AUTHORIZED_CAP"],
                            bins=[0, 1e6, 1e7, 1e8, float("inf")],
                            labels=["Small", "Medium", "Large", "Very Large"])
print("Added COMPANY_AGE and CAPITAL_SIZE:")
print(df[["COMPANY_NAME", "COMPANY_AGE", "CAPITAL_SIZE"]].head())

# remove variables
before = df.shape[1]
df = df.drop(columns=["REGISTERED_STATE", "EMAIL_ADDR"])
print(f"\nColumns before: {before}, after dropping 2 columns: {df.shape[1]}")

# add a case (row)
new_row = {c: None for c in df.columns}
new_row.update({"COMPANY_NAME": "Demo New Company Pvt Ltd", "COMPANY_STATUS": "Active",
                "COMPANY_CLASS": "Private", "AUTHORIZED_CAP": 500000})
rows_before = len(df)
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
print(f"Rows before adding case: {rows_before}, after: {len(df)}")

# remove cases (rows)
df = df[df["COMPANY_NAME"] != "Demo New Company Pvt Ltd"]
df = df.dropna(subset=["DATE_OF_REGISTRATION"]).reset_index(drop=True)
print("Rows after removing demo row / rows with no date:", len(df))

# ------------------------------------------------ 7. SORTING AND SHUFFLING
print("\n=== 7. SORTING AND SHUFFLING ===")
print("Top 5 by Authorized Capital (descending):")
print(df.sort_values("AUTHORIZED_CAP", ascending=False)[
    ["COMPANY_NAME", "AUTHORIZED_CAP"]].head())

print("\nSorted by Class (asc) then Capital (desc):")
print(df.sort_values(["COMPANY_CLASS", "AUTHORIZED_CAP"], ascending=[True, False])[
    ["COMPANY_NAME", "COMPANY_CLASS", "AUTHORIZED_CAP"]].head())

shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
print("\nAfter shuffling (first 5 names):")
print(shuffled["COMPANY_NAME"].head().tolist())

# ----------------------------------------------------------------- SAVE
df.to_csv("gujarat_companies_prepared.csv", index=False)
print("\nPrepared data saved to gujarat_companies_prepared.csv  Shape:", df.shape)
