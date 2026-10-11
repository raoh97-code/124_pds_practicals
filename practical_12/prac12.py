import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from retail_data import load_retail

df = load_retail()
rng = np.random.default_rng(42)
pop_mean, pop_std = df.Revenue.mean(), df.Revenue.std()
print(f"Population: N={len(df)}, mean revenue/line={pop_mean:.3f}, std={pop_std:.3f}")

# ============ (a) SAMPLING TECHNIQUES ============
n = 2000
random_s = df.sample(n=n, random_state=1)                                   # simple random

step = len(df) // n                                                         # systematic
start = rng.integers(0, step)
systematic_s = df.iloc[start::step]

stratified_s = df.groupby("Country").sample(frac=n / len(df), random_state=1)   # proportional stratified by Country

res = pd.DataFrame({
    "Sample size": [len(random_s), len(systematic_s), len(stratified_s)],
    "Mean Revenue": [random_s.Revenue.mean(), systematic_s.Revenue.mean(), stratified_s.Revenue.mean()],
    "Std Revenue": [random_s.Revenue.std(), systematic_s.Revenue.std(), stratified_s.Revenue.std()],
    "Abs error vs population mean": [abs(s.Revenue.mean() - pop_mean) for s in (random_s, systematic_s, stratified_s)],
}, index=["Random", "Systematic", "Stratified (Country)"])
print("\n", res.round(3))
print("\nCountry share (%) - population vs stratified sample (top 5):")
print(pd.concat([df.Country.value_counts(normalize=True).mul(100).rename("Population"),
                 stratified_s.Country.value_counts(normalize=True).mul(100).rename("Stratified")],
                axis=1).head(5).round(2))

# ============ (b) POINT & INTERVAL ESTIMATION ============
samp = df.sample(n=500, random_state=7)
x = samp.Revenue
m, s, nn = x.mean(), x.std(ddof=1), len(x)
se = s / np.sqrt(nn)
print("\n--- Point estimates ---")
print(f"Mean = {m:.3f}, Std dev = {s:.3f}, Median = {x.median():.3f}")
p_hat = (samp.Country == "United Kingdom").mean()
print(f"Proportion of UK transactions (p̂) = {p_hat:.3f}")

print("\n--- Interval estimates ---")
for cl in (0.90, 0.95, 0.99):
    lo, hi = stats.t.interval(cl, df=nn - 1, loc=m, scale=se)
    print(f"{int(cl*100)}% CI for mean revenue/line: ({lo:.3f}, {hi:.3f})")
z = stats.norm.ppf(0.975); me = z * np.sqrt(p_hat * (1 - p_hat) / nn)
print(f"95% CI for UK proportion: ({p_hat - me:.3f}, {p_hat + me:.3f})   [true = {(df.Country=='United Kingdom').mean():.3f}]")
boot = [rng.choice(x, nn).mean() for _ in range(5000)]
print(f"Bootstrap 95% CI for mean: ({np.percentile(boot, 2.5):.3f}, {np.percentile(boot, 97.5):.3f})")
print(f"True population mean = {pop_mean:.3f}")

# ============ (c) CENTRAL LIMIT THEOREM ============
pop = df.Revenue.values
sizes = [2, 5, 30, 100]
fig, ax = plt.subplots(1, 5, figsize=(24, 4))
ax[0].hist(np.clip(pop, 0, np.percentile(pop, 99)), bins=60, color="grey")
ax[0].set_title("Population (skewed), clipped at 99th pct")
for a, k in zip(ax[1:], sizes):
    means = rng.choice(pop, size=(3000, k)).mean(axis=1)
    a.hist(means, bins=50, density=True, alpha=.6)
    xs = np.linspace(means.min(), means.max(), 300)
    a.plot(xs, stats.norm.pdf(xs, pop_mean, pop_std / np.sqrt(k)), "r", lw=2)
    a.set_title(f"Sample means, n={k}")
    print(f"n={k:3d}: mean of means={means.mean():.3f} (μ={pop_mean:.3f}) | "
          f"SD of means={means.std():.3f} (σ/√n={pop_std/np.sqrt(k):.3f}) | skew={stats.skew(means):.2f}")
plt.tight_layout(); plt.show()
print("As n grows, the sampling distribution becomes bell-shaped and narrower (σ/√n), "
      "even though the population is highly skewed -> Central Limit Theorem.")

# ============ (d) ONE-SAMPLE t-TEST ============
alpha = 0.05
test_sample = df.sample(n=500, random_state=11).Revenue
for mu0 in (20, 25):
    t, p = stats.ttest_1samp(test_sample, popmean=mu0)
    print(f"\nH0: μ = {mu0}   vs   H1: μ ≠ {mu0}")
    print(f"sample mean={test_sample.mean():.3f}, t={t:.3f}, p-value={p:.4f}")
    print("Decision:", "Reject H0 (significant difference)" if p < alpha else "Fail to reject H0 (no significant evidence)",
          f"at α={alpha}")
t, p = stats.ttest_1samp(test_sample, 20, alternative="greater")
print(f"\nOne-sided test (H1: μ > 20): t={t:.3f}, p={p:.4f}")