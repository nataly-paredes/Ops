# Power BI DAX Measures — Operations Dashboard

All measures are organized by report page. Each includes the business purpose and the DAX formula.

---

## Page 1: Executive Summary

### SLA Compliance %
> % of orders fulfilled within the 24-hour SLA window.
```dax
SLA Compliance % =
DIVIDE(
    COUNTROWS(FILTER(warehouse_operations, warehouse_operations[sla_met] = TRUE())),
    COUNTROWS(warehouse_operations),
    0
) * 100
```

### Avg Throughput vs Benchmark
> Compares actual throughput to the 120 uph benchmark. Negative = below target.
```dax
Throughput Gap =
AVERAGE(warehouse_operations[throughput_uph]) - 120
```

### Avg Dock Delay (hrs)
```dax
Avg Dock Delay =
AVERAGE(warehouse_operations[dock_delay_hrs])
```

### Total Operational Cost
```dax
Total Cost =
SUMX(
    warehouse_operations,
    warehouse_operations[cost_per_unit] * warehouse_operations[units_processed]
)
```

### KPI Status (conditional)
> Used to drive conditional formatting on KPI cards (Green / Red).
```dax
SLA Status =
IF([SLA Compliance %] >= 95, "On Target", "Below Target")
```

---

## Page 2: Regional Breakdown

### Throughput by Region (ranked)
```dax
Region Throughput Rank =
RANKX(
    ALL(warehouse_operations[region]),
    CALCULATE(AVERAGE(warehouse_operations[throughput_uph])),
    ,
    DESC,
    DENSE
)
```

### Region vs Benchmark Flag
```dax
Below Throughput Benchmark =
IF(
    AVERAGE(warehouse_operations[throughput_uph]) < 120,
    "Below Benchmark",
    "On Target"
)
```

### Revenue at Risk (Region 3 estimate)
> Simulates lost revenue from throughput shortfall vs benchmark.
```dax
Revenue at Risk =
VAR BenchmarkUPH = 120
VAR ActualUPH = AVERAGE(warehouse_operations[throughput_uph])
VAR UnitShortfall = MAX(BenchmarkUPH - ActualUPH, 0)
VAR AvgRevenuePerUnit = 12.50  -- configurable assumption
RETURN
    SUMX(
        warehouse_operations,
        UnitShortfall * AvgRevenuePerUnit
    )
```

---

## Page 3: Shift Analysis

### Defect Rate by Shift
```dax
Defect Rate % =
AVERAGE(warehouse_operations[defect_rate_pct])
```

### Night Shift Defect Premium
> How much higher is night shift defect rate vs. day shift?
```dax
Night Shift Defect Premium =
VAR NightRate =
    CALCULATE(
        AVERAGE(warehouse_operations[defect_rate_pct]),
        warehouse_operations[shift] = "Night"
    )
VAR DayRate =
    CALCULATE(
        AVERAGE(warehouse_operations[defect_rate_pct]),
        warehouse_operations[shift] = "Day"
    )
RETURN
    DIVIDE(NightRate - DayRate, DayRate, 0) * 100
```

---

## Page 5: What-If Projection

### What-If: Dock Delay Reduction
> Uses a Power BI What-If Parameter (0–100% reduction slider).
```dax
Projected Dock Delay =
[Avg Dock Delay] * (1 - 'Delay Reduction %'[Delay Reduction % Value] / 100)
```

### Projected SLA Improvement
```dax
Projected SLA % =
VAR DelayReduction = 'Delay Reduction %'[Delay Reduction % Value] / 100
VAR ProjectedDelay = [Avg Dock Delay] * (1 - DelayReduction)
VAR ImprovementFactor = IF(ProjectedDelay < 2, 1.15, 1.05)
RETURN
    MIN([SLA Compliance %] * ImprovementFactor, 100)
```

### Projected Cost Savings
```dax
Projected Annual Savings =
VAR CurrentCost = [Total Cost]
VAR DefectReductionFactor = 0.50  -- assume 50% defect reduction from shift SOP alignment
VAR DefectCostShare = 0.22        -- 22% of OpEx tied to defects (as identified)
RETURN
    CurrentCost * DefectCostShare * DefectReductionFactor
```
