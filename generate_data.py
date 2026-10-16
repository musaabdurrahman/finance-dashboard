import numpy as np
import pandas as pd

rng = np.random.default_rng(42)  # fixed seed so results are reproducible
dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
rows = []


def spend(mean, sigma=0.5):
    """Right-skewed amounts: mostly small, occasionally large, like real spending."""
    return round(rng.lognormal(np.log(mean), sigma), 2)


# Salary paid on the 25th, or the Friday before if the 25th is a weekend
paydays = set()
for month_start in pd.date_range("2025-01-01", "2025-12-01", freq="MS"):
    payday = month_start + pd.Timedelta(days=24)
    while payday.weekday() >= 5:
        payday -= pd.Timedelta(days=1)
    paydays.add(payday)

for d in dates:
    weekend = d.weekday() >= 5
    december = d.month == 12
    winter = d.month in (11, 12, 1, 2)

    # Day-to-day spending
    if rng.random() < 0.6:
        rows.append((d, "Food", spend(10), "Expense"))
    if not weekend and rng.random() < 0.8:
        rows.append((d, "Transport", spend(4, 0.3), "Expense"))
    if rng.random() < (0.25 if weekend else 0.05):
        rows.append((d, "Entertainment", spend(20), "Expense"))
    if rng.random() < (0.25 if december else 0.07):  # Christmas spike
        rows.append((d, "Shopping", spend(35, 0.8), "Expense"))

    # Irregular side income
    if rng.random() < 0.08:
        rows.append((d, "Freelance", float(rng.choice([25, 30, 40, 60])), "Income"))

    # Fixed monthly items
    if d.day == 1:
        rows.append((d, "Rent", 600.00, "Expense"))
    if d.day == 15:
        rows.append((d, "Utilities", spend(110 if winter else 65, 0.15), "Expense"))
    if d in paydays:
        salary = 1800.00 if d.month < 7 else 1900.00  # pay rise in July
        rows.append((d, "Salary", salary, "Income"))
    if d.day == 28:
        rows.append((d, "Savings", 300.00, "Transfer"))

# One-off events
one_offs = [
    ("2025-03-14", "Shopping", 420.00),  # new phone
    ("2025-08-09", "Travel", 650.00),    # summer holiday
    ("2025-10-03", "Health", 85.00),     # dentist
]
for date, category, amount in one_offs:
    rows.append((pd.Timestamp(date), category, amount, "Expense"))

df = pd.DataFrame(rows, columns=["Date", "Category", "Amount", "Type"])
df = df.sort_values("Date")
df.to_csv("transactions.csv", index=False)
print(f"Generated {len(df)} transactions")