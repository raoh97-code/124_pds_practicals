import sys, os, re
import numpy as np, pandas as pd

def load_data():
    DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "gujarat_companies.csv")
    df = pd.read_csv(DATA_PATH, low_memory=False, encoding_errors="replace",
                     na_values=["", " ", "NA", "N/A", "NULL", "null", "-"])
    df.columns = [re.sub(r"\W+", "_", str(c).strip()).strip("_").upper() for c in df.columns]
    for c in df.select_dtypes("object"):
        df[c] = df[c].astype("string").str.strip()

    def find(*keys):
        for c in df.columns:
            if all(k in c for k in keys):
                return c
        raise KeyError(f"No column matching {keys}")

    C = dict(
        STATUS=find("COMPANY", "STATUS"),
        CLASS=find("COMPANY", "CLASS"),
        SUBCAT=find("SUB", "CATEGORY"),
        DATE=find("DATE", "REGISTRATION"),
        AUTH=find("AUTH"),
        PAID=find("PAID"),
        PBA=find("PRINCIPAL", "BUSINESS"),
        ROC=find("REGISTRAR"),
    )
    df[C["DATE"]] = pd.to_datetime(df[C["DATE"]], dayfirst=True, errors="coerce")
    for k in ("AUTH", "PAID"):
        df[C[k]] = pd.to_numeric(df[C[k]], errors="coerce")
    df["YEAR"] = df[C["DATE"]].dt.year
    return df, C

pd.set_option("display.width", 200); pd.set_option("display.max_columns", 50)
df, C = load_data()
print("Detected columns:", C)

# ============ (a) DESCRIBE DATASET & DATA TYPES ============
print("Shape:", df.shape)
print(df.head())
df.info()
print("\nData type of each attribute:\n", df.dtypes)
print("\nNumeric summary:\n", df.describe().T)
print("\nCategorical summary:\n", df.select_dtypes(include=["object", "string"]).describe().T)
print("\nUnique values per column:\n", df.nunique())
print("\nDuplicate rows:", df.duplicated().sum())

# ============ (b) MISSING VALUES ============
miss = df.isnull().sum().to_frame("Missing")
miss["Missing %"] = (miss.Missing / len(df) * 100).round(2)
print("\nMissing values:\n", miss[miss.Missing > 0].sort_values("Missing", ascending=False))

# --- Handling methods ---
# Method 1: drop columns with > 60% missing, then drop rows without a registration date
m1 = df.drop(columns=miss.index[miss["Missing %"] > 60])
m1 = m1.dropna(subset=[C["DATE"]])
print("\nMethod 1 (drop sparse columns / rows w/o date):", m1.shape)

# Method 2: impute - numeric -> median, categorical -> 'Unknown'
m2 = df.copy()
for c in m2.select_dtypes(include=np.number).columns:
    if c != "YEAR":
        m2[c] = m2[c].fillna(m2[c].median())
for c in m2.select_dtypes(include=["object", "string"]).columns:
    m2[c] = m2[c].fillna("Unknown")
print("Method 2 (median / 'Unknown' imputation) - missing left:", int(m2.drop(columns=["YEAR", C["DATE"]]).isnull().sum().sum()))

# Method 3: compare imputation strategies on a numeric column
a = df[C["AUTH"]]
cmp = pd.DataFrame({"Original mean": [a.mean()],
                    "After mean-fill": [a.fillna(a.mean()).mean()],
                    "After median-fill": [a.fillna(a.median()).mean()],
                    "After ffill": [a.ffill().mean()]})
print("\nEffect of imputation on", C["AUTH"], "\n", cmp)

# Method 4: categorical -> mode
st = df[C["STATUS"]].fillna(df[C["STATUS"]].mode()[0])

# ============ (c) DESCRIPTIVE STATISTICS ============
numeric = [C["AUTH"], C["PAID"]]
rows = {}
for c in numeric:
    x = df[c].dropna()
    q1, q3 = x.quantile([.25, .75])
    rows[c] = {
        # central tendency
        "Mean": x.mean(), "Median": x.median(), "Mode": x.mode().iloc[0],
        # dispersion
        "Min": x.min(), "Max": x.max(), "Range": x.max() - x.min(),
        "Variance": x.var(), "Std Dev": x.std(), "IQR": q3 - q1,
        "Coeff. of Variation (%)": x.std() / x.mean() * 100,
        # location
        "Q1 (25th)": q1, "Q3 (75th)": q3, "P10": x.quantile(.10), "P90": x.quantile(.90), "P99": x.quantile(.99),
        # shape & symmetry
        "Skewness": x.skew(), "Kurtosis (excess)": x.kurt(),
    }
stats_tbl = pd.DataFrame(rows)
print("\n", stats_tbl.round(2))
for c in numeric:
    sk = stats_tbl.loc["Skewness", c]
    print(f"{c}: skewness={sk:.2f} -> {'right-skewed' if sk > .5 else 'left-skewed' if sk < -.5 else 'roughly symmetric'}; "
          f"mean {'>' if stats_tbl.loc['Mean', c] > stats_tbl.loc['Median', c] else '<='} median")