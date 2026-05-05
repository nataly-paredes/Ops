"""
generate_mock_data.py
Generates synthetic warehouse operations data for the Operations Pain Point Dashboard.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# Config
N_RECORDS = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 12, 31)

REGIONS = {
    "Region 1 - Northeast":    {"throughput_factor": 1.05, "defect_factor": 0.90},
    "Region 2 - Southeast":    {"throughput_factor": 1.00, "defect_factor": 1.00},
    "Region 3 - Mid-Atlantic": {"throughput_factor": 0.72, "defect_factor": 1.30},  # problem region
    "Region 4 - Midwest":      {"throughput_factor": 0.98, "defect_factor": 0.95},
    "Region 5 - South":        {"throughput_factor": 1.02, "defect_factor": 1.05},
}

SHIFTS = {
    "Day":   {"defect_multiplier": 1.0,  "dock_delay_multiplier": 1.0},
    "Night": {"defect_multiplier": 2.1,  "dock_delay_multiplier": 1.4},  # night shift problem
}

SLA_TARGET_HOURS = 24


def random_date(start, end):
    return start + timedelta(seconds=np.random.randint(0, int((end - start).total_seconds())))


def generate_data():
    records = []

    for _ in range(N_RECORDS):
        region_name = np.random.choice(list(REGIONS.keys()))
        region = REGIONS[region_name]

        shift_name = np.random.choice(list(SHIFTS.keys()), p=[0.6, 0.4])
        shift = SHIFTS[shift_name]

        order_date = random_date(START_DATE, END_DATE)

        # Throughput (units per hour) — benchmark is 120
        throughput = round(np.random.normal(120 * region["throughput_factor"], 10), 1)
        throughput = max(50, throughput)

        # Dock delay (hours)
        base_delay = np.random.exponential(2.0)
        dock_delay = round(base_delay * shift["dock_delay_multiplier"] * (1.4 if region_name == "Region 3 - Mid-Atlantic" else 1.0), 2)

        # Defect rate (%)
        base_defect = np.random.normal(2.3, 0.5)
        defect_rate = round(base_defect * region["defect_factor"] * shift["defect_multiplier"], 2)
        defect_rate = max(0, defect_rate)

        # Inventory accuracy (%)
        if region_name in ["Region 3 - Mid-Atlantic", "Region 5 - South"]:
            inv_accuracy = round(np.random.normal(92.5, 2.0), 1)
        else:
            inv_accuracy = round(np.random.normal(97.0, 1.5), 1)
        inv_accuracy = min(100, max(80, inv_accuracy))

        # SLA (hours to fulfill)
        sla_hours = round(dock_delay + np.random.normal(18, 3), 1)
        sla_met = sla_hours <= SLA_TARGET_HOURS

        # Cost per unit
        cost_per_unit = round(np.random.normal(4.50, 0.80) * (1 + defect_rate / 100), 2)
        cost_per_unit = max(2.0, cost_per_unit)

        records.append({
            "order_id":          f"ORD-{np.random.randint(100000, 999999)}",
            "order_date":        order_date.strftime("%Y-%m-%d"),
            "month":             order_date.strftime("%Y-%m"),
            "region":            region_name,
            "shift":             shift_name,
            "throughput_uph":    throughput,
            "dock_delay_hrs":    dock_delay,
            "defect_rate_pct":   defect_rate,
            "inventory_accuracy_pct": inv_accuracy,
            "sla_hours":         sla_hours,
            "sla_met":           sla_met,
            "cost_per_unit":     cost_per_unit,
            "units_processed":   np.random.randint(50, 500),
        })

    df = pd.DataFrame(records)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/warehouse_operations_raw.csv", index=False)
    print(f"✅ Generated {len(df)} records → data/raw/warehouse_operations_raw.csv")
    return df


if __name__ == "__main__":
    df = generate_data()
    print("\nSample:")
    print(df.head(3).to_string())
    print(f"\nShape: {df.shape}")
    print(f"\nRegion throughput averages:")
    print(df.groupby("region")["throughput_uph"].mean().round(1))
