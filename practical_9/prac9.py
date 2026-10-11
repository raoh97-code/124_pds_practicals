import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
from scipy import stats
from retail_data import load_retail

sns.set_theme(style="whitegrid")
df = load_retail()
num = ["Quantity", "UnitPrice", "Revenue"]
print(df.shape); print(df.head())

# ======================= UNIVARIATE =======================
print("\n--- Descriptive statistics ---")
print(df[num].describe().T)
print("\nSkewness:\n", df[num].skew())
print("\nKurtosis:\n", df[num].kurt())

q99 = df[num].quantile(0.99)
fig, ax = plt.subplots(2, 3, figsize=(15, 8))
for i, c in enumerate(num):
    x = df.loc[df[c] <= q99[c], c]
    sns.histplot(x, bins=50, kde=True, ax=ax[0, i]); ax[0, i].set_title(f"Histogram of {c} (≤ 99th pct)")
    sns.boxplot(x=x, ax=ax[1, i]);                   ax[1, i].set_title(f"Boxplot of {c} (≤ 99th pct)")
plt.tight_layout(); plt.show()

# categorical variables
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
df["Country"].value_counts().head(10).plot(kind="bar", ax=ax[0], title="Top 10 countries by transactions")
df["InvoiceDate"].dt.month.value_counts().sort_index().plot(kind="bar", ax=ax[1], title="Transactions per month")
plt.tight_layout(); plt.show()
print("UK share of transactions: %.1f%%" % (100 * (df.Country == "United Kingdom").mean()))

# ======================= BIVARIATE =======================
sm = df[(df.Quantity <= q99.Quantity) & (df.UnitPrice <= q99.UnitPrice)].sample(5000, random_state=1)
plt.figure(figsize=(7, 5))
sns.scatterplot(data=sm, x="UnitPrice", y="Quantity", alpha=.4)
plt.title("Quantity vs UnitPrice"); plt.show()

print("\nPearson  (Quantity, UnitPrice):", stats.pearsonr(df.Quantity, df.UnitPrice))
print("Spearman (Quantity, UnitPrice):", stats.spearmanr(df.Quantity, df.UnitPrice))

fig, ax = plt.subplots(1, 3, figsize=(18, 5))
df.groupby("Country")["Revenue"].sum().nlargest(10).plot(kind="bar", ax=ax[0], title="Top-10 countries by revenue")
df.groupby(df.InvoiceDate.dt.to_period("M"))["Revenue"].sum().plot(ax=ax[1], marker="o", title="Monthly revenue")
df.groupby(df.InvoiceDate.dt.hour)["Revenue"].sum().plot(kind="bar", ax=ax[2], title="Revenue by hour of day")
plt.tight_layout(); plt.show()

df["is_uk"] = np.where(df.Country == "United Kingdom", "UK", "Non-UK")
uk, non = df.loc[df.is_uk == "UK", "Revenue"], df.loc[df.is_uk == "Non-UK", "Revenue"]
print("\nMean revenue/line  UK: %.2f | Non-UK: %.2f" % (uk.mean(), non.mean()))
print("Mann-Whitney U (UK vs Non-UK revenue):", stats.mannwhitneyu(uk, non))

# ======================= MULTIVARIATE =======================
cust = (df.dropna(subset=["CustomerID"]).groupby("CustomerID")
          .agg(TotalQty=("Quantity", "sum"), TotalRevenue=("Revenue", "sum"),
               NumInvoices=("InvoiceNo", "nunique"), AvgUnitPrice=("UnitPrice", "mean"),
               NumProducts=("StockCode", "nunique"), Country=("Country", "first")))
cust["Region"] = np.where(cust.Country == "United Kingdom", "UK", "Non-UK")
feat = ["TotalQty", "TotalRevenue", "NumInvoices", "AvgUnitPrice", "NumProducts"]
logc = np.log1p(cust[feat])

sns.pairplot(pd.concat([logc, cust["Region"]], axis=1), hue="Region", corner=True,
             plot_kws={"alpha": .4, "s": 15})
plt.suptitle("Pair plot of customer features (log scale)", y=1.02); plt.show()

plt.figure(figsize=(7, 5))
sns.heatmap(logc.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation heatmap (customer level, log-scaled)"); plt.show()

# 3 variables together: weekday x hour -> revenue
pv = df.pivot_table(index=df.InvoiceDate.dt.day_name(), columns=df.InvoiceDate.dt.hour,
                    values="Revenue", aggfunc="sum")
pv = pv.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"])
plt.figure(figsize=(12, 4)); sns.heatmap(pv, cmap="YlOrRd"); plt.title("Revenue: weekday × hour"); plt.show()

# ======================= INTERPRETATION =======================
print("\n--- Interpretation ---")
for c in num:
    print(f"{c}: skew={df[c].skew():.1f} -> strongly right-skewed (few very large values); "
          f"mean {df[c].mean():.2f} > median {df[c].median():.2f}")
print("Quantity & UnitPrice are weakly (negatively) related: cheap items are bought in bulk.")
print("Revenue is dominated by the UK; sales peak around midday and in Oct-Nov (pre-Christmas).")
print("Customer features (qty, revenue, invoices, products) are strongly positively correlated.")