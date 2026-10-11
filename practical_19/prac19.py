import os
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

SHOW = True
os.makedirs("output", exist_ok=True)
sns.set_theme(style="whitegrid")

# single shared dataset: <project>/data/gujarat_companies.csv
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "gujarat_companies.csv"
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.upper()
df = df.drop_duplicates()
df["DATE_OF_REGISTRATION"] = pd.to_datetime(df["DATE_OF_REGISTRATION"],
                                            format="%d-%m-%Y", errors="coerce")
df["REG_YEAR"] = df["DATE_OF_REGISTRATION"].dt.year
df = df.dropna(subset=["AUTHORIZED_CAP", "PAIDUP_CAPITAL"])
df["LOG_AUTH_CAP"] = np.log10(df["AUTHORIZED_CAP"])
df["LOG_PAIDUP_CAP"] = np.log10(df["PAIDUP_CAPITAL"].clip(lower=1))
ACT = "PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN"


def finish(name):
    plt.tight_layout()
    plt.savefig(f"output/{name}.png", dpi=150)
    if SHOW:
        plt.show()
    plt.close()


# ----------------------------------------------------------- a) BAR PLOT
sub = df[df["COMPANY_CLASS"].isin(["Private", "Public"])]
pct = (sub.groupby(ACT)["COMPANY_CLASS"].value_counts(normalize=True)
       .mul(100).rename("PERCENT").reset_index())
plt.figure(figsize=(11, 6))
sns.barplot(data=pct, y=ACT, x="PERCENT", hue="COMPANY_CLASS", palette="Set2")
plt.xlabel("Percentage of companies (%)")
plt.ylabel("Principal business activity")
plt.title("Private vs Public companies (%) by Principal Business Activity")
finish("19a_barplot")

# --------------------------------------------------------- b) STRIP PLOT
plt.figure(figsize=(9, 6))
sample = df.sample(1500, random_state=1)            # sample keeps the plot readable
sns.stripplot(data=sample, x="COMPANY_CLASS", y="AUTHORIZED_CAP", jitter=0.25,
              alpha=0.5, size=3, palette="Set1", hue="COMPANY_CLASS", legend=False)
plt.yscale("log")
plt.xlabel("Company class")
plt.ylabel("Authorized capital (INR, log scale)")
plt.title("Strip plot: Authorized Capital by Company Class (1500-company sample)")
finish("19b_stripplot")

# --------------------------------------------------------- c) VIOLIN PLOT
plt.figure(figsize=(9, 6))
sns.violinplot(data=df, x="COMPANY_CLASS", y="LOG_AUTH_CAP", inner="quartile",
               palette="muted", hue="COMPANY_CLASS", legend=False)
plt.xlabel("Company class")
plt.ylabel("log10(Authorized capital)")
plt.title("Violin plot: Distribution of Authorized Capital across Company Classes")
finish("19c_violinplot")

# ---------------------------------------------------------- d) PAIR PLOT
pair_cols = ["LOG_AUTH_CAP", "LOG_PAIDUP_CAP", "REG_YEAR"]
g = sns.pairplot(df.sample(1500, random_state=2)[pair_cols + ["COMPANY_CLASS"]],
                 hue="COMPANY_CLASS", diag_kind="kde",
                 plot_kws={"alpha": 0.5, "s": 15})
g.figure.suptitle("Pair plot of numeric attributes", y=1.02)
g.savefig("output/19d_pairplot.png", dpi=150)
if SHOW:
    plt.show()
plt.close("all")

# ----------------------------------------------------------- e) KDE PLOT
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
sns.kdeplot(data=df, x="LOG_AUTH_CAP", hue="COMPANY_CLASS", fill=True,
            common_norm=False, alpha=0.4, ax=ax[0])
ax[0].set_title("KDE of Authorized Capital by Company Class")
ax[0].set_xlabel("log10(Authorized capital)")
sns.kdeplot(data=df, x="LOG_AUTH_CAP", hue="COMPANY_STATUS", common_norm=False,
            ax=ax[1], legend=True)
ax[1].set_title("KDE of Authorized Capital by Company Status")
ax[1].set_xlabel("log10(Authorized capital)")
finish("19e_kdeplot")

print("""
INTERPRETATION NOTES
- Bar plot   : compares percentage of private vs public companies per activity.
- Strip plot : each dot is a company; shows individual values and density.
- Violin plot: combines a boxplot (quartiles) with a KDE to show the shape.
- Pair plot  : scatter plots of every pair plus distribution on the diagonal.
- KDE plot   : smooth estimate of the probability density of authorized capital.
(Capital is plotted on a log scale because it is highly right-skewed.)
All figures saved in the 'output' folder.""")
