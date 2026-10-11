import os, io, zipfile, urllib.request
import numpy as np
import pandas as pd

CACHE = "online_retail_cache.csv"
UCI_ZIP = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
COLS = ["InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country"]


def _download():
    # Try 1: ucimlrepo package (dataset id 352 = Online Retail)
    try:
        from ucimlrepo import fetch_ucirepo
        df = fetch_ucirepo(id=352).data.features.copy()
        if all(c in df.columns for c in COLS):
            return df[COLS]
    except Exception as e:
        print("ucimlrepo failed, using direct download:", e)
    # Try 2: direct zip from UCI
    raw = urllib.request.urlopen(UCI_ZIP).read()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        name = [n for n in z.namelist() if n.lower().endswith(".xlsx")][0]
        return pd.read_excel(z.open(name))[COLS]


def load_retail(clean=True):
    """Returns the Online Retail dataset (cached after the first download).
    clean=True removes cancelled invoices, returns, zero prices and adds Revenue."""
    if os.path.exists(CACHE):
        df = pd.read_csv(CACHE, dtype={"InvoiceNo": str, "StockCode": str})
    else:
        df = _download()
        df.to_csv(CACHE, index=False)
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    if clean:
        df = df[~df["InvoiceNo"].str.startswith("C")]
        df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
        df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    return df.reset_index(drop=True)