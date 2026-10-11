
import os
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

SHOW = True
os.makedirs("output", exist_ok=True)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

# single shared dataset: <project>/data/gujarat_companies.csv
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "gujarat_companies.csv"
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.upper()
df = df.drop_duplicates()
df["DATE_OF_REGISTRATION"] = pd.to_datetime(df["DATE_OF_REGISTRATION"],
                                            format="%d-%m-%Y", errors="coerce")
df["REG_YEAR"] = df["DATE_OF_REGISTRATION"].dt.year
df["COMPANY_AGE"] = 2026 - df["REG_YEAR"]
df = df.dropna(subset=["AUTHORIZED_CAP", "PAIDUP_CAPITAL", "REG_YEAR"])
df["PAIDUP_RATIO"] = df["PAIDUP_CAPITAL"] / df["AUTHORIZED_CAP"]

num_cols = ["AUTHORIZED_CAP", "PAIDUP_CAPITAL", "REG_YEAR", "COMPANY_AGE", "PAIDUP_RATIO"]
num = df[num_cols]

# ------------------------------------------------- a) COVARIANCE AND PEARSON
print("=== a) COVARIANCE MATRIX ===")
print(num.cov())
print("\n=== PEARSON CORRELATION MATRIX ===")
corr = num.corr(method="pearson")
print(corr.round(3))

print("\nInterpretation:")
print("- Correlation lies between -1 and +1; covariance depends on the units.")
print(f"- AUTHORIZED_CAP vs PAIDUP_CAPITAL r = {corr.loc['AUTHORIZED_CAP', 'PAIDUP_CAPITAL']:.3f} "
      "(paid-up capital can never exceed authorized capital).")
print(f"- REG_YEAR vs COMPANY_AGE r = {corr.loc['REG_YEAR', 'COMPANY_AGE']:.3f} "
      "(perfect negative: age is derived from year).")

# -------------------------------------------------------------- b) HEATMAP
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1,
            linewidths=0.5, square=True)
plt.title("Pearson correlation heatmap")
plt.tight_layout()
plt.savefig("output/correlation_heatmap.png", dpi=150)
if SHOW:
    plt.show()
plt.close()


# ------------------------------------------------------- c) CHI-SQUARE TESTS
def chi_square(col1, col2, alpha=0.05):
    table = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, expected = chi2_contingency(table)
    print(f"\n--- {col1}  vs  {col2} ---")
    print(table)
    print(f"chi2 = {chi2:.3f}, degrees of freedom = {dof}, p-value = {p:.4f}")
    if (expected < 5).any():
        print("Note: some expected counts < 5, so the result is approximate.")
    if p < alpha:
        print(f"Result: p < {alpha} -> reject H0: the variables are DEPENDENT (associated).")
    else:
        print(f"Result: p >= {alpha} -> fail to reject H0: no evidence of association "
              "(variables independent).")


print("\n=== c) CHI-SQUARE TEST FOR INDEPENDENCE ===")
print("H0: the two categorical variables are independent. H1: they are associated.")
chi_square("COMPANY_CLASS", "COMPANY_STATUS")
chi_square("COMPANY_CLASS", "REGISTRAR_OF_COMPANIES")
chi_square("COMPANY_STATUS", "PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN")
print("\nAll figures saved in the 'output' folder.")
