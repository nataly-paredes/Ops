# 🏭 Operations Pain Point Dashboard
### Warehouse & Logistics Performance Analysis | Power BI + DAX + SQL

---

## 📖 The Business Story

A regional logistics company operating across 5 warehouse locations was experiencing **rising operational costs, missed SLAs, and inconsistent throughput** across sites — but leadership had no unified view of where the problems were or why they were happening.

As the BI Engineer on this engagement, I was brought in to:
1. Identify where the pain points lived (region, shift, process type)
2. Quantify the cost and time impact
3. Build a dashboard that told that story clearly to both operations managers and executives
4. Project what improvements would look like if corrective actions were taken

---

## 🔍 Pain Points Identified

| Pain Point | Impact |
|---|---|
| Receiving dock delays averaging 3.2 hrs | Downstream delays in pick/pack by 40% |
| Region 3 (Mid-Atlantic) throughput 28% below benchmark | $180K+ monthly revenue at risk |
| Night shift defect rate 2.1x higher than day shift | Rework costs inflating OpEx by 22% |
| Inventory accuracy below 94% in 2 of 5 locations | Order fulfillment errors up 18% |

---

## 💡 The "After" Story — Recommended Actions & Projected Impact

| Recommendation | Projected Improvement |
|---|---|
| Stagger receiving dock schedules | Reduce dock delay by 65% |
| Cross-train night shift on day shift SOPs | Reduce defect rate gap by 50% |
| Implement cycle count program (weekly) | Inventory accuracy to 98%+ |
| Add Regional KPI accountability in weekly ops review | 15% throughput improvement within 90 days |

---

## 📁 Project Structure

```
project1-ops-dashboard/
│
├── data/
│   ├── raw/
│   │   └── warehouse_operations_raw.csv       # Mock raw dataset
│   └── cleaned/
│       └── warehouse_operations_clean.csv     # Post-processing output
│
├── sql/
│   ├── 01_create_tables.sql                   # Schema setup
│   ├── 02_data_quality_checks.sql             # Validation queries
│   ├── 03_kpi_metrics.sql                     # Core KPI calculations
│   └── 04_regional_benchmarking.sql           # Regional comparison logic
│
├── python/
│   ├── generate_mock_data.py                  # Mock dataset generator
│   ├── data_cleaning.py                       # Cleaning & transformation
│   └── eda_analysis.py                        # Exploratory data analysis
│
├── powerbi/
│   ├── dax_measures.md                        # All DAX measures documented
│   └── dashboard_screenshots/                 # Dashboard visuals
│
└── README.md
```

---

## 🛠️ Tools & Technologies

- **SQL Server** — data modeling, KPI queries, optimization
- **Python (pandas, matplotlib, seaborn)** — data cleaning, EDA, visualization
- **Power BI + DAX** — interactive dashboard, drill-throughs, KPI cards
- **Excel / CSV** — mock data source

---

## 📊 Dashboard Pages

1. **Executive Summary** — Overall KPIs: throughput, SLA %, cost per unit, defect rate
2. **Regional Breakdown** — Side-by-side comparison across 5 locations
3. **Shift Analysis** — Day vs. night performance across key metrics
4. **Trend Analysis** — 12-month view of throughput, errors, and dock delays
5. **"What If" Projection** — Modeled impact of recommended changes

---

## 🔑 Key DAX Measures

See [`powerbi/dax_measures.md`](powerbi/dax_measures.md) for full documentation.

Highlights:
- `SLA Compliance %` — % of orders fulfilled within target window
- `Throughput vs. Benchmark` — dynamic comparison using benchmark reference table
- `Defect Rate by Shift` — filtered measure with shift slicer support
- `Projected Savings` — what-if parameter driving scenario modeling

---

## 📈 Key Outcomes (Simulated)

- Reduced average dock delay from **3.2 hrs → 1.1 hrs** after schedule change
- Night shift defect rate dropped **from 4.8% → 2.3%** after SOP alignment
- Region 3 throughput improved **28% → benchmark parity** within 90 days
- Dashboard replaced **3 manual weekly reports**, saving ~12 hours/week

---

## 🚀 How to Run

```bash
# 1. Generate mock data
python python/generate_mock_data.py

# 2. Clean and prepare data
python python/data_cleaning.py

# 3. Run EDA
python python/eda_analysis.py

# 4. Load cleaned CSV into SQL Server using 01_create_tables.sql
# 5. Run KPI queries in order (02 → 03 → 04)
# 6. Connect Power BI to SQL Server or use cleaned CSV directly
```

---

*This project uses fully synthetic data generated for portfolio demonstration purposes.*
