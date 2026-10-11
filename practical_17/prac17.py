import os
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

SHOW = True
os.makedirs("output", exist_ok=True)

# single shared dataset: <project>/data/gujarat_companies.csv
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "gujarat_companies.csv"
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.upper()
df = df.drop_duplicates()
df["DATE_OF_REGISTRATION"] = pd.to_datetime(df["DATE_OF_REGISTRATION"],
                                            format="%d-%m-%Y", errors="coerce")
df["REG_YEAR"] = df["DATE_OF_REGISTRATION"].dt.year
ACT = "PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN"


def finish(name):
    plt.tight_layout()
    plt.savefig(f"output/{name}.png", dpi=150)
    if SHOW:
        plt.show()
    plt.close()


# ------------------------------------------------------------- a) PIE CHART
fig, ax = plt.subplots(1, 2, figsize=(13, 6))
status = df["COMPANY_STATUS"].value_counts()
ax[0].pie(status, labels=status.index, autopct="%1.1f%%", startangle=90,
          textprops={"fontsize": 8})
ax[0].set_title("Percentage of companies by Company Status")
cls = df["COMPANY_CLASS"].value_counts()
ax[1].pie(cls, labels=cls.index, autopct="%1.1f%%", startangle=90,
          explode=[0.05] * len(cls), textprops={"fontsize": 8})
ax[1].set_title("Percentage of companies by Company Class")
finish("17a_pie_chart")

# -------------------------------------------------------------- b) BAR CHART
sub = df[df["COMPANY_CLASS"].isin(["Private", "Public"])]
pct = (pd.crosstab(sub[ACT], sub["COMPANY_CLASS"], normalize="index") * 100)
pct.plot(kind="barh", figsize=(11, 6), color=["#1f77b4", "#ff7f0e"])
plt.xlabel("Percentage of companies (%)")
plt.ylabel("Principal business activity")
plt.title("Private vs Public companies (%) by Principal Business Activity")
plt.legend(title="Class")
finish("17b_bar_chart")

# ------------------------------------------------------------ c) HISTOGRAM
# Registrar is categorical, so a count histogram (bar of counts) is drawn
roc = df["REGISTRAR_OF_COMPANIES"].value_counts()
plt.figure(figsize=(8, 5))
plt.bar(roc.index, roc.values, color="seagreen", edgecolor="black", width=1.0)
plt.xlabel("Registrar of Companies")
plt.ylabel("Number of companies")
plt.title("Companies with respect to Registrar of Companies")
finish("17c_histogram")

# --------------------------------------------------------------- d) BOXPLOT
plt.figure(figsize=(9, 5))
plt.boxplot(df["AUTHORIZED_CAP"].dropna(), showfliers=True)
plt.yscale("log")
plt.ylabel("Authorized capital (INR, log scale)")
plt.title("Boxplot of Authorized Capital")
plt.xticks([])
finish("17d_boxplot")

# ------------------------------------------------------------ e) SCATTERPLOT
plt.figure(figsize=(9, 5))
codes = df["REGISTRAR_OF_COMPANIES"].astype("category")
plt.scatter(codes.cat.codes + np.random.uniform(-0.15, 0.15, len(df)),
            df["AUTHORIZED_CAP"], s=8, alpha=0.4, c=codes.cat.codes, cmap="tab10")
plt.xticks(range(len(codes.cat.categories)), codes.cat.categories)
plt.yscale("log")
plt.xlabel("Registrar of Companies (small jitter added)")
plt.ylabel("Authorized capital (INR, log scale)")
plt.title("Authorized Capital vs Registrar of Companies")
finish("17e_scatterplot")

# ---------------------------------------------------------------- f) LINE
yearly = df.groupby("REG_YEAR").size()
plt.figure(figsize=(10, 5))
plt.plot(yearly.index, yearly.values, marker="o", color="crimson")
plt.xlabel("Year of registration")
plt.ylabel("Number of companies registered")
plt.title("Year-wise trend of company registrations")
plt.grid(alpha=0.3)
finish("17f_line_chart")

# ---------------------------------------------------------------- g) AREA
cumulative = yearly.cumsum()
plt.figure(figsize=(10, 5))
plt.fill_between(cumulative.index, cumulative.values, alpha=0.5, color="teal")
plt.plot(cumulative.index, cumulative.values, color="teal")
plt.xlabel("Year")
plt.ylabel("Cumulative number of companies")
plt.title("Cumulative companies registered over the years")
finish("17g_area_chart")

# ------------------------------------------------ COMPARISON (APPLICABILITY)
print("""
COMPARISON OF CHARTS WITH RESPECT TO APPLICABILITY
--------------------------------------------------
Pie chart   : Shows share of a whole; good for few categories (<=6). Hard to read
              when there are many slices or similar-sized slices.
Bar chart   : Compares values across categories; works for many categories and
              for side-by-side comparison (private vs public).
Histogram   : Shows the frequency distribution of a variable (numeric data in bins);
              here used as counts per registrar.
Boxplot     : Summarises spread (median, quartiles, outliers) of ONE numeric
              variable; best for spotting outliers such as huge authorized capitals.
Scatterplot : Shows the relationship between two variables / groups; with
              categorical X it shows the spread of capital within each registrar.
Line chart  : Best for time-series. The line connects ordered points so the
              trend (rise/fall) over years is easy to follow.
Area chart  : Like a line chart but the filled area emphasises magnitude; ideal
              for cumulative totals over time.
""")
print("Line chart suits time series because time is continuous and ordered; the "
      "connecting line shows direction, rate of change and seasonality that "
      "separate bars or points do not.")
print("\nAll figures saved in the 'output' folder.")
