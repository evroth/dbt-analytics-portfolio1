import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure output directory exists
os.makedirs("data/raw", exist_ok=True)

np.random.seed(42)

# -------------------------
# Customers
# -------------------------
customers = pd.DataFrame({
    "customer_id": range(1, 101),
    "signup_date": [
        datetime(2023, 1, 1) + timedelta(days=int(x))
        for x in np.random.randint(0, 365, 100)
    ],
    "plan": np.random.choice(["Free", "Pro", "Enterprise"], 100),
    "region": np.random.choice(["NA", "EMEA", "APAC"], 100)
})

# -------------------------
# Subscriptions
# -------------------------
subscriptions = pd.DataFrame({
    "subscription_id": range(1, 101),
    "customer_id": customers["customer_id"],
    "monthly_revenue": customers["plan"].map({
        "Free": 0,
        "Pro": 50,
        "Enterprise": 200
    }),
    "is_active": np.random.choice([True, False], 100, p=[0.8, 0.2])
})

# -------------------------
# Save CSVs
# -------------------------
customers.to_csv("data/raw/customers.csv", index=False)
subscriptions.to_csv("data/raw/subscriptions.csv", index=False)

print("Data generated successfully.")
