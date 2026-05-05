"""
eda_analysis.py
Exploratory Data Analysis for the Operations Pain Point Dashboard.
Produces charts that mirror the Power BI story arc:
  1. KPI summary
  2. Regional performance comparison
  3. Shift analysis (day vs. night)
  4. Trend over time
  5. Correlation heatmap
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

sns.set_theme(style="whitegrid", palette="Blues_d")
BLUE = "#1F4E79"
ORANGE = "#C55A11"
GREEN = "#375623"
LIGHT_BLUE = "#9DC3E6"

OUTPUT_DIR = "python/eda_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load(path="data/cleaned/warehouse_operations_clean.csv"):
    df = pd.read_csv(path, parse_dates=["order_date"])
    print(f"Loaded cleaned data: {df.shape}")
    return df


# ── 1. KPI Summary ────────────────────────────────────────────────────────────
def plot_kpi_summary(df):
    kpis = {
        "Avg Throughput\n(units/hr)":   df["throughput_uph"].mean(),
        "Avg Dock Delay\n(hrs)":         df["dock_delay_hrs"].mean(),
        "Avg Defect Rate\n(%)":          df["defect_rate_pct"].mean(),
        "SLA Compliance\n(%)":           df["sla_met_flag"].mean() * 100,
        "Inv. Accuracy\n(%)":            df["inventory_accuracy_pct"].mean(),
    }
    targets = {
        "Avg Throughput\n(units/hr)":   120,
        "Avg Dock Delay\n(hrs)":         1.0,
        "Avg Defect Rate\n(%)":          2.0,
        "SLA Compliance\n(%)":           95,
        "Inv. Accuracy\n(%)":            98,
    }

    fig, axes = plt.subplots(1, 5, figsize=(16, 4))
    fig.suptitle("Operations KPI Summary vs. Targets", fontsize=14, fontweight="bold", color=BLUE)

    for ax, (label, value) in zip(axes, kpis.items()):
        target = targets[label]
        color = GREEN if (
            (label in ["Avg Throughput\n(units/hr)", "SLA Compliance\n(%)", "Inv. Accuracy\n(%)"] and value >= target) or
            (label in ["Avg Dock Delay\n(hrs)", "Avg Defect Rate\n(%)"] and value <= target)
        ) else ORANGE
        ax.text(0.5, 0.55, f"{value:.1f}", ha="center", va="center",
                fontsize=26, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.25, f"Target: {target}", ha="center", va="center",
                fontsize=10, color="gray", transform=ax.transAxes)
        ax.set_title(label, fontsize=10, color=BLUE)
        ax.axis("off")

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/01_kpi_summary.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


# ── 2. Regional Comparison ────────────────────────────────────────────────────
def plot_regional_comparison(df):
    region_stats = df.groupby("region_short").agg(
        throughput=("throughput_uph", "mean"),
        defect_rate=("defect_rate_pct", "mean"),
        sla_pct=("sla_met_flag", lambda x: x.mean() * 100),
        dock_delay=("dock_delay_hrs", "mean"),
    ).reset_index().sort_values("throughput")

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    fig.suptitle("Regional Performance Comparison", fontsize=14, fontweight="bold", color=BLUE)

    metrics = [
        ("throughput", "Avg Throughput (units/hr)", BLUE, True),
        ("defect_rate", "Avg Defect Rate (%)", ORANGE, False),
        ("sla_pct", "SLA Compliance (%)", BLUE, True),
        ("dock_delay", "Avg Dock Delay (hrs)", ORANGE, False),
    ]

    for ax, (col, title, color, higher_better) in zip(axes, metrics):
        bars = ax.barh(region_stats["region_short"], region_stats[col], color=LIGHT_BLUE)
        worst_idx = region_stats[col].idxmin() if higher_better else region_stats[col].idxmax()
        bars[region_stats.index.get_loc(worst_idx)].set_color(ORANGE)
        ax.set_title(title, fontsize=10, color=BLUE)
        ax.set_xlabel("")
        ax.tick_params(labelsize=8)

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/02_regional_comparison.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


# ── 3. Shift Analysis ─────────────────────────────────────────────────────────
def plot_shift_analysis(df):
    shift_stats = df.groupby("shift").agg(
        defect_rate=("defect_rate_pct", "mean"),
        dock_delay=("dock_delay_hrs", "mean"),
        throughput=("throughput_uph", "mean"),
        sla_pct=("sla_met_flag", lambda x: x.mean() * 100),
    ).reset_index()

    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    fig.suptitle("Day Shift vs. Night Shift Performance", fontsize=14, fontweight="bold", color=BLUE)

    metrics = ["defect_rate", "dock_delay", "throughput", "sla_pct"]
    titles = ["Defect Rate (%)", "Dock Delay (hrs)", "Throughput (uph)", "SLA Compliance (%)"]
    colors = [ORANGE, ORANGE, BLUE, BLUE]

    for ax, col, title, color in zip(axes, metrics, titles, colors):
        ax.bar(shift_stats["shift"], shift_stats[col], color=[LIGHT_BLUE, color])
        ax.set_title(title, fontsize=10, color=BLUE)
        ax.tick_params(labelsize=9)
        for bar in ax.patches:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.3,
                    f"{bar.get_height():.1f}",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/03_shift_analysis.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


# ── 4. Monthly Trend ──────────────────────────────────────────────────────────
def plot_monthly_trend(df):
    monthly = df.groupby("month_num").agg(
        throughput=("throughput_uph", "mean"),
        defect_rate=("defect_rate_pct", "mean"),
        sla_pct=("sla_met_flag", lambda x: x.mean() * 100),
        dock_delay=("dock_delay_hrs", "mean"),
    ).reset_index()

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly["month_label"] = monthly["month_num"].apply(lambda x: months[x-1])

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("12-Month Operational Trend", fontsize=14, fontweight="bold", color=BLUE)

    pairs = [
        (axes[0,0], "throughput", "Avg Throughput (uph)", BLUE),
        (axes[0,1], "defect_rate", "Avg Defect Rate (%)", ORANGE),
        (axes[1,0], "sla_pct", "SLA Compliance (%)", BLUE),
        (axes[1,1], "dock_delay", "Avg Dock Delay (hrs)", ORANGE),
    ]

    for ax, col, title, color in pairs:
        ax.plot(monthly["month_label"], monthly[col], marker="o", color=color, linewidth=2)
        ax.fill_between(monthly["month_label"], monthly[col], alpha=0.1, color=color)
        ax.set_title(title, fontsize=10, color=BLUE)
        ax.tick_params(axis="x", rotation=45, labelsize=8)

    plt.tight_layout()
    path = f"{OUTPUT_DIR}/04_monthly_trend.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


# ── 5. Correlation Heatmap ────────────────────────────────────────────────────
def plot_correlation_heatmap(df):
    cols = ["throughput_uph", "dock_delay_hrs", "defect_rate_pct",
            "inventory_accuracy_pct", "cost_per_unit", "sla_met_flag"]
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", ax=ax,
                linewidths=0.5, vmin=-1, vmax=1)
    ax.set_title("KPI Correlation Heatmap", fontsize=13, fontweight="bold", color=BLUE)
    plt.tight_layout()
    path = f"{OUTPUT_DIR}/05_correlation_heatmap.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


if __name__ == "__main__":
    df = load()
    print("\nRunning EDA...\n")
    plot_kpi_summary(df)
    plot_regional_comparison(df)
    plot_shift_analysis(df)
    plot_monthly_trend(df)
    plot_correlation_heatmap(df)
    print(f"\n✅ All charts saved to {OUTPUT_DIR}/")
