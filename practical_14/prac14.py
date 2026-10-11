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

pd.set_option("display.width", 220); pd.set_option("display.max_columns", 50); pd.set_option("display.max_rows", 200)
df, C = load_data()
df = df.dropna(subset=[C["DATE"]])
AUTH, PAID = C["AUTH"], C["PAID"]
AGG = ["count", "mean", "median", "std", "min", "max", "sum"]

def summarize(d, title):
    print("\n" + "=" * 90 + f"\n{title}\nRecords: {len(d)}\n" + "=" * 90)
    if len(d):
        print(d[[AUTH, PAID]].agg(AGG).T.round(2))

# a) Registered between 2010 and 2015 (inclusive)
a = df[df.YEAR.between(2010, 2015)]
summarize(a, "(a) Companies registered 2010-2015")
print("\nCompanies registered per year:\n", a.YEAR.value_counts().sort_index())

# b) Principal business = Finance AND registered after 2016 (i.e. 2017 onwards)
b = df[df[C["PBA"]].str.contains("financ", case=False, na=False) & (df.YEAR > 2016)]
summarize(b, "(b) Finance companies registered after 2016")
print("\nPrincipal-business values matched:", b[C["PBA"]].unique())

# c) By principal business activity, registered 2015-2017 (inclusive)
c = df[df.YEAR.between(2015, 2017)]
print("\n" + "=" * 90 + "\n(c) Principal business activity-wise, registered 2015-2017\n" + "=" * 90)
print(c.groupby(C["PBA"])[[AUTH, PAID]].agg(AGG).round(2))
print("\nCompany count per activity:\n", c[C["PBA"]].value_counts())

# d) Group by Company Status
print("\n" + "=" * 90 + "\n(d) Grouped by Company Status\n" + "=" * 90)
print(df.groupby(C["STATUS"])[[AUTH, PAID]].agg(AGG).round(2))
print("\nShare (%):\n", df[C["STATUS"]].value_counts(normalize=True).mul(100).round(2))

# e) Group by Company Status + Company Sub-category
print("\n" + "=" * 90 + "\n(e) Grouped by Company Status and Sub-category\n" + "=" * 90)
e = df.groupby([C["STATUS"], C["SUBCAT"]])[[AUTH, PAID]].agg(AGG).round(2)
print(e)
print("\nCross-tab of counts:\n", pd.crosstab(df[C["STATUS"]], df[C["SUBCAT"]]))