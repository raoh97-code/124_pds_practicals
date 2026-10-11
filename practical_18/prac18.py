import os
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

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

# ----------------------------------------------- a) GRIDSPEC UNEVEN LAYOUT
fig = plt.figure(figsize=(15, 10))
gs = GridSpec(3, 3, figure=fig, height_ratios=[1.2, 1, 1], width_ratios=[2, 1, 1])

# big plot spanning the whole top row
ax1 = fig.add_subplot(gs[0, :])
yearly = df.groupby("REG_YEAR").size()
ax1.plot(yearly.index, yearly.values, marker="o", color="crimson")
ax1.fill_between(yearly.index, yearly.values, alpha=0.2, color="crimson")
ax1.set_title("Companies registered per year")
ax1.set_xlabel("Year")
ax1.set_ylabel("Count")

# tall plot on the left spanning two rows
ax2 = fig.add_subplot(gs[1:, 0])
act = df[ACT].value_counts().sort_values()
ax2.barh(act.index, act.values, color="steelblue")
ax2.set_title("Companies by principal business activity")
ax2.tick_params(axis="y", labelsize=7)

# small plots on the right
ax3 = fig.add_subplot(gs[1, 1])
status = df["COMPANY_STATUS"].value_counts()
ax3.pie(status, labels=status.index, autopct="%1.0f%%", textprops={"fontsize": 6})
ax3.set_title("Company status")

ax4 = fig.add_subplot(gs[1, 2])
cls = df["COMPANY_CLASS"].value_counts()
ax4.bar(range(len(cls)), cls.values, color=["#4c72b0", "#dd8452", "#55a868"])
ax4.set_xticks(range(len(cls)))
ax4.set_xticklabels(["Private", "Public", "OPC"][:len(cls)] if len(cls) == 3 else cls.index,
                    fontsize=8)
ax4.set_title("Company class")

ax5 = fig.add_subplot(gs[2, 1:])
ax5.hist(np.log10(df["AUTHORIZED_CAP"].dropna()), bins=40, color="seagreen",
         edgecolor="white")
ax5.set_title("Distribution of authorized capital (log10 INR)")
ax5.set_xlabel("log10(Authorized capital)")

fig.suptitle("Company Master Data of Gujarat - Overview Dashboard", fontsize=16)
fig.tight_layout(rect=[0, 0, 1, 0.96])

# c) SAVE AT HIGH RESOLUTION
fig.savefig("output/gridspec_dashboard.png", dpi=300)
fig.savefig("output/gridspec_dashboard.pdf", dpi=300)
if SHOW:
    plt.show()
plt.close(fig)

# --------------------------------------------------- b) DUAL-AXIS (TWIN Y)
per_year = df.groupby("REG_YEAR").agg(companies=("COMPANY_NAME", "count"),
                                      avg_cap=("AUTHORIZED_CAP", "mean"))
fig, ax_left = plt.subplots(figsize=(11, 6))
ax_left.bar(per_year.index, per_year["companies"], color="lightsteelblue",
            label="Companies registered")
ax_left.set_xlabel("Year of registration")
ax_left.set_ylabel("Number of companies", color="steelblue")
ax_left.tick_params(axis="y", labelcolor="steelblue")

ax_right = ax_left.twinx()                       # second y-axis sharing the x-axis
ax_right.plot(per_year.index, per_year["avg_cap"] / 1e6, color="darkred",
              marker="o", label="Average authorized capital")
ax_right.set_ylabel("Average authorized capital (INR million)", color="darkred")
ax_right.tick_params(axis="y", labelcolor="darkred")

lines = ax_left.get_legend_handles_labels()
lines2 = ax_right.get_legend_handles_labels()
ax_left.legend(lines[0] + lines2[0], lines[1] + lines2[1], loc="upper left")
plt.title("Companies registered vs average authorized capital per year")
fig.tight_layout()

fig.savefig("output/dual_axis_chart.png", dpi=300)
fig.savefig("output/dual_axis_chart.pdf", dpi=300)
if SHOW:
    plt.show()
plt.close(fig)

print("Saved (300 dpi): output/gridspec_dashboard.png/.pdf and "
      "output/dual_axis_chart.png/.pdf")
