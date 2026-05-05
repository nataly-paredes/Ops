"""
data_cleaning.py
Cleans and transforms raw warehouse operations data for analysis and Power BI ingestion.
"""

import pandas as pd
import numpy as np
import os

def load_raw(path="data/raw/warehouse_operations_raw.csv"):
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows, {df.shape[1]} columns")
    return df


def flag_data_quality_issues(df):
    """Identify and log data quality issues before cleaning."""
    issues = {}
    issues["null_counts"] = df.isnull().sum().to_dict()
    issues["duplicate_order_ids"] = df.duplicated(subset=["order_id"]).sum()
    issues["negative_throughput"] = (df["throughput_uph"] < 0).sum()
    issues["defect_rate_over_100"] = (df["defect_rate_pct"] > 100).sum()
    issues["inv_accuracy_out_of_range"] = ((df["inventory_accuracy_pct"] < 0) | (df["inventory_accuracy_pct"] > 100)).sum()

    print("\n📋 Data Quality Report:")
    for k, v in issues.items():
        print(f"  {k}: {v}")
    return issues


def clean(df):
    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["order_id"])
    print(f"\nDropped {before - len(df)} duplicate order IDs")

    # Clamp out-of-range values
    df["defect_rate_pct"] = df["defect_rate_pct"].clip(lower=0, upper=100)
    df["inventory_accuracy_pct"] = df["inventory_accuracy_pct"].clip(lower=0, upper=100)
    df["throughput_uph"] = df["throughput_uph"].clip(lower=0)
    df["cost_per_unit"] = df["cost_per_unit"].clip(lower=0)

    # Parse dates
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year"] = df["order_date"].dt.year
    df["quarter"] = df["order_date"].dt.quarter
    df["month_num"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.strftime("%b")
    df["week"] = df["order_date"].dt.isocalendar().week.astype(int)

    # Derived KPIs
    df["sla_met_flag"] = df["sla_met"].astype(int)
    df["is_night_shift"] = (df["shift"] == "Night").astype(int)
    df["total_cost"] = (df["cost_per_unit"] * df["units_processed"]).round(2)
    df["dock_delay_category"] = pd.cut(
        df["dock_delay_hrs"],
        bins=[0, 1, 2, 4, 100],
        labels=["<1hr", "1-2hrs", "2-4hrs", ">4hrs"]
    )

    # Region short name
    df["region_short"] = df["region"].str.extract(r"Region (\d+) - (.+)").apply(
        lambda x: f"R{x[0]} {x[1]}" if pd.notna(x[0]) else x[1], axis=1
    )

    # Benchmark flags
    THROUGHPUT_BENCHMARK = 120
    df["below_throughput_benchmark"] = (df["throughput_uph"] < THROUGHPUT_BENCHMARK).astype(int)
    df["high_defect_flag"] = (df["defect_rate_pct"] > 3.5).astype(int)
    df["low_inv_accuracy_flag"] = (df["inventory_accuracy_pct"] < 94).astype(int)

    return df


def save_clean(df, path="data/cleaned/warehouse_operations_clean.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"\n✅ Clean data saved → {path}")
    print(f"   Final shape: {df.shape}")


if __name__ == "__main__":
    df = load_raw()
    flag_data_quality_issues(df)
    df_clean = clean(df)
    save_clean(df_clean)

    print("\n📊 Summary Statistics:")
    print(df_clean[["throughput_uph", "dock_delay_hrs", "defect_rate_pct",
                     "inventory_accuracy_pct", "cost_per_unit"]].describe().round(2))
