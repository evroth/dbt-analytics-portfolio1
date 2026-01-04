import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure output directory exists
os.makedirs("data/raw", exist_ok=True)

np.random.seed(42)

n_customers = 500
customer_ids = range(1, n_customers + 1)

# -------------------------
# Customers
# -------------------------
customers = pd.DataFrame({
    "customer_id": customer_ids,
    "signup_date": (
        datetime(2021, 1, 1)
        + pd.to_timedelta(np.random.randint(0, 1000, n_customers), unit="D")
    ),
    "industry": np.random.choice(["Tech", "Finance", "Healthcare"], n_customers),
    "segment": np.random.choice(["SMB", "Mid", "Enterprise"], n_customers),
})

# -------------------------
# Subscriptions
# -------------------------
subscription_rows = []
subscription_id_counter = 1

for _, cust in customers.iterrows():
    customer_id = cust.customer_id
    signup_date = cust.signup_date

    # ---- Initial subscription ----
    initial_plan = np.random.choice(
        ["Free", "Pro", "Enterprise"],
        p=[0.4, 0.4, 0.2]
    )

    created_at = signup_date
    end_date = None

    # Chance of churn without plan change
    churned_initially = np.random.rand() < 0.15

    if churned_initially:
        end_date = created_at + timedelta(days=np.random.randint(90, 720))

    subscription_rows.append({
        "subscription_id": subscription_id_counter,
        "customer_id": customer_id,
        "plan": initial_plan,
        "created_at": created_at,
        "end_date": end_date
    })

    previous_subscription_id = subscription_id_counter
    subscription_id_counter += 1

    # ---- Optional plan change (only if not churned) ----
    if not churned_initially and np.random.rand() < 0.25:
        change_date = created_at + timedelta(days=np.random.randint(90, 540))

        # Close previous subscription at change date
        subscription_rows[-1]["end_date"] = change_date

        new_plan = np.random.choice(
            [p for p in ["Free", "Pro", "Enterprise"] if p != initial_plan]
        )

        new_end_date = None

        # Chance of churn after plan change
        if np.random.rand() < 0.15:
            new_end_date = change_date + timedelta(days=np.random.randint(90, 720))

        subscription_rows.append({
            "subscription_id": subscription_id_counter,
            "customer_id": customer_id,
            "plan": new_plan,
            "created_at": change_date,
            "end_date": new_end_date
        })

        subscription_id_counter += 1

subscriptions = pd.DataFrame(subscription_rows)

# -------------------------
# Invoices
# -------------------------
PLAN_PRICING = {
    "Free": 0,
    "Pro": 250,
    "Enterprise": 800
}

invoice_cutoff_date = customers["signup_date"].max() + timedelta(days=30)

invoice_rows = []
invoice_id_counter = 1

for _, sub in subscriptions.iterrows():
    start_date = sub.created_at

    # Cap billing at churn date or global cutoff (whichever is earlier)
    end_date = min(
        sub.end_date if pd.notna(sub.end_date) else invoice_cutoff_date,
        invoice_cutoff_date
    )

    current_date = start_date

    while current_date < end_date:
        invoice_rows.append({
            "invoice_id": invoice_id_counter,
            "subscription_id": sub.subscription_id,
            "invoice_date": current_date,
            "amount": PLAN_PRICING[sub.plan],
            "type": "recurring"
        })
        invoice_id_counter += 1
        current_date += timedelta(days=30)


invoices = pd.DataFrame(invoice_rows)

# -------------------------
# Save CSVs
# -------------------------
customers.to_csv("data/raw/customers.csv", index=False)
subscriptions.to_csv("data/raw/subscriptions.csv", index=False)
invoices.to_csv("data/raw/invoices.csv", index=False)

print("Data generated successfully.")
