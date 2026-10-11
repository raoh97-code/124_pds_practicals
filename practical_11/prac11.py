import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from retail_data import load_retail

df = load_retail()
inv = (df.groupby("InvoiceNo")
         .agg(InvoiceDate=("InvoiceDate", "min"), Total=("Revenue", "sum"))
         .reset_index().sort_values("InvoiceDate"))

# ===================== (a) NORMAL =====================
# Raw invoice totals are heavily skewed, so use log10(invoice total) which is ~normal
x = np.log10(inv.Total[inv.Total > 0])
mu, sigma = stats.norm.fit(x)
print(f"Fitted Normal on log10(Invoice Total): mu={mu:.3f}, sigma={sigma:.3f}")
print(f"Skewness={x.skew():.3f}, Excess kurtosis={x.kurt():.3f}")
print("KS test vs fitted normal:", stats.kstest(x, stats.norm(mu, sigma).cdf))
print(f"P(invoice between £50 and £500) = "
      f"{stats.norm.cdf(np.log10(500), mu, sigma) - stats.norm.cdf(np.log10(50), mu, sigma):.4f}")

g = np.linspace(x.min(), x.max(), 400)
fig, ax = plt.subplots(1, 4, figsize=(20, 4.5))
ax[0].plot(g, stats.norm.pdf(g, mu, sigma)); ax[0].set_title("Normal PDF")
ax[1].plot(g, stats.norm.cdf(g, mu, sigma), label="Theoretical")
ax[1].plot(np.sort(x), np.arange(1, len(x) + 1) / len(x), "--", label="Empirical"); ax[1].set_title("Normal CDF"); ax[1].legend()
ax[2].hist(x, bins=50, density=True, alpha=.6, label="Data")
ax[2].plot(g, stats.norm.pdf(g, mu, sigma), "r", lw=2, label="Fitted Normal"); ax[2].set_title("Histogram + Normal fit"); ax[2].legend()
ax[2].set_xlabel("log10(Invoice Total)")
stats.probplot(x, dist="norm", plot=ax[3]); ax[3].set_title("Q-Q plot")
plt.tight_layout(); plt.show()

# ===================== (b) EXPONENTIAL =====================
# Time between consecutive invoices (minutes). Keep gaps within trading hours (0 < gap <= 60 min)
gaps = inv.InvoiceDate.diff().dt.total_seconds().div(60).dropna()
gaps = gaps[(gaps > 0) & (gaps <= 60)]
loc, scale = stats.expon.fit(gaps, floc=0)
lam = 1 / scale
print(f"\nFitted Exponential: scale (mean gap)={scale:.3f} min, rate λ={lam:.4f} per min")
print("KS test vs fitted exponential:", stats.kstest(gaps, "expon", args=(0, scale)))
print(f"P(next invoice arrives within 5 min)  = {stats.expon.cdf(5, 0, scale):.4f}")
print(f"P(wait more than 15 min)               = {stats.expon.sf(15, 0, scale):.4f}")

t = np.linspace(0, gaps.max(), 400)
fig, ax = plt.subplots(1, 3, figsize=(17, 4.5))
ax[0].plot(t, stats.expon.pdf(t, 0, scale)); ax[0].set_title("Exponential PDF")
ax[1].plot(t, stats.expon.cdf(t, 0, scale), label="Theoretical")
ax[1].plot(np.sort(gaps), np.arange(1, len(gaps) + 1) / len(gaps), "--", label="Empirical"); ax[1].set_title("Exponential CDF"); ax[1].legend()
ax[2].hist(gaps, bins=40, density=True, alpha=.6, label="Data")
ax[2].plot(t, stats.expon.pdf(t, 0, scale), "r", lw=2, label="Fitted Exponential")
ax[2].set(title="Histogram + Exponential fit", xlabel="Minutes between invoices"); ax[2].legend()
plt.tight_layout(); plt.show()
print("Note: timestamps are recorded to the minute, so a few ties (gap = 0) are excluded; "
      "the fit is approximate because the arrival rate varies across the day.")