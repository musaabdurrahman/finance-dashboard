import numpy as np
import pandas as pd

rng = np.random.default_rng(42)  # fixed seed so results are reproducible
dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
rows = []

for d in dates:
    # Variable day-to-day spending
    if rng.random() < 0.6:
        rows.append((d, "Food", round(rng.uniform(4, 25), 2), "Expense"))
    if d.weekday() < 5 and rng.random() < 0.8:
        rows.append((d, "Transport", round(rng.uniform(2.5, 6), 2), "Expense"))
    if rng.random() < 0.1:
        rows.append((d, "Entertainment", round(rng.uniform(8, 40), 2), "Expense"))
    if rng.random() < 0.08:
        rows.append((d, "Shopping", round(rng.uniform(10, 120), 2), "Expense"))

    # Fixed monthly items
    if d.day == 1:
        rows.append((d, "Rent", 600.00, "Expense"))
    if d.day == 15:
        rows.append((d, "Utilities", round(rng.uniform(60, 110), 2), "Expense"))
    if d.day == 25:
        rows.append((d, "Salary", 1800.00, "Income"))
    if d.day == 28:
        rows.append((d, "Savings", 300.00, "Transfer"))

df = pd.DataFrame(rows, columns=["Date", "Category", "Amount", "Type"])
df.to_csv("transactions.csv", index=False)
print(f"Generated {len(df)} transactions")