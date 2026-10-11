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

# ===================== (a) BINOMIAL =====================
# Experiment: pick n=10 invoices; "success" = high-value invoice (total >= £500)
THRESH, n = 500, 10
inv["success"] = (inv.Total >= THRESH).astype(int)
p = inv.success.mean()
rng = np.random.default_rng(42)
shuffled = rng.permutation(inv.success.values)            # shuffle -> trials ~ independent
k = len(shuffled) // n
blocks = shuffled[:k * n].reshape(k, n).sum(axis=1)       # successes in each group of 10

x = np.arange(n + 1)
pmf, cdf = stats.binom.pmf(x, n, p), stats.binom.cdf(x, n, p)
obs = np.bincount(blocks, minlength=n + 1) / k
obs_cdf = np.cumsum(obs)

print(f"p(success)={p:.4f}, n={n}, groups={k}")
print(pd.DataFrame({"x": x, "Theoretical PMF": pmf.round(4), "Observed prop": obs.round(4),
                    "Theoretical CDF": cdf.round(4), "Observed CDF": obs_cdf.round(4)}))
print(f"Theoretical mean={n*p:.3f}, var={n*p*(1-p):.3f} | Observed mean={blocks.mean():.3f}, var={blocks.var():.3f}")
print(f"P(X>=3) = {1 - stats.binom.cdf(2, n, p):.4f}")

fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
w = 0.4
ax[0].bar(x - w/2, pmf, w, label="Theoretical PMF"); ax[0].bar(x + w/2, obs, w, label="Observed proportion")
ax[0].set(title=f"Binomial PMF (n={n}, p={p:.3f})", xlabel="Successes", ylabel="Probability"); ax[0].legend()
ax[1].step(x, cdf, where="post", label="Theoretical CDF"); ax[1].step(x, obs_cdf, where="post", ls="--", label="Observed CDF")
ax[1].set(title="Binomial CDF", xlabel="Successes", ylabel="Cumulative probability"); ax[1].legend()
plt.tight_layout(); plt.show()

# ===================== (b) POISSON =====================
# Experiment: number of invoices raised in each 1-hour slot (10:00-15:59) of each trading day
inv["date"], inv["hour"] = inv.InvoiceDate.dt.date, inv.InvoiceDate.dt.hour
HOURS = range(10, 16)
cnt = inv[inv.hour.isin(HOURS)].groupby(["date", "hour"]).size()
full = pd.MultiIndex.from_product([inv.date.unique(), HOURS], names=["date", "hour"])
cnt = cnt.reindex(full, fill_value=0)
lam = cnt.mean()

kmax = int(cnt.max())
xs = np.arange(kmax + 1)
pmf, cdf = stats.poisson.pmf(xs, lam), stats.poisson.cdf(xs, lam)
obs = np.bincount(cnt.values, minlength=kmax + 1) / len(cnt)
obs_cdf = np.cumsum(obs)

print(f"\nlambda (mean invoices/hour) = {lam:.3f}, variance = {cnt.var():.3f}, "
      f"dispersion index var/mean = {cnt.var()/lam:.2f}  (≈1 for ideal Poisson)")
print(f"P(X=5)={stats.poisson.pmf(5, lam):.4f},  P(X<=3)={stats.poisson.cdf(3, lam):.4f},  P(X>8)={stats.poisson.sf(8, lam):.4f}")

fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
ax[0].bar(xs - w/2, pmf, w, label="Theoretical PMF"); ax[0].bar(xs + w/2, obs, w, label="Observed proportion")
ax[0].set(title=f"Poisson PMF (λ={lam:.2f})", xlabel="Invoices per hour", ylabel="Probability"); ax[0].legend()
ax[1].step(xs, cdf, where="post", label="Theoretical CDF"); ax[1].step(xs, obs_cdf, where="post", ls="--", label="Observed CDF")
ax[1].set(title="Poisson CDF", xlabel="Invoices per hour", ylabel="Cumulative probability"); ax[1].legend()
plt.tight_layout(); plt.show()
print("Interpretation: if the dispersion index is well above 1, hourly counts vary more than a pure Poisson "
      "process (arrival rate changes through the day / seasons), so the fit is only approximate.")