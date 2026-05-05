-- ============================================================
-- 03_kpi_metrics.sql
-- Core KPI calculations for Operations Dashboard
-- ============================================================

-- ── Overall KPI Summary ───────────────────────────────────────
SELECT
    COUNT(*)                                            AS total_orders,
    ROUND(AVG(throughput_uph), 1)                       AS avg_throughput_uph,
    ROUND(AVG(dock_delay_hrs), 2)                       AS avg_dock_delay_hrs,
    ROUND(AVG(defect_rate_pct), 2)                      AS avg_defect_rate_pct,
    ROUND(AVG(inventory_accuracy_pct), 1)               AS avg_inv_accuracy_pct,
    ROUND(CAST(SUM(CAST(sla_met AS INT)) AS FLOAT)
          / COUNT(*) * 100, 1)                          AS sla_compliance_pct,
    ROUND(AVG(cost_per_unit), 2)                        AS avg_cost_per_unit,
    ROUND(SUM(cost_per_unit * units_processed), 0)      AS total_cost
FROM warehouse_operations;


-- ── KPIs by Region ───────────────────────────────────────────
SELECT
    wo.region,
    COUNT(*)                                                    AS total_orders,
    ROUND(AVG(wo.throughput_uph), 1)                            AS avg_throughput,
    ROUND(AVG(wo.dock_delay_hrs), 2)                            AS avg_dock_delay,
    ROUND(AVG(wo.defect_rate_pct), 2)                           AS avg_defect_rate,
    ROUND(AVG(wo.inventory_accuracy_pct), 1)                    AS avg_inv_accuracy,
    ROUND(CAST(SUM(CAST(wo.sla_met AS INT)) AS FLOAT)
          / COUNT(*) * 100, 1)                                  AS sla_compliance_pct,
    -- Gap vs. benchmark
    ROUND(AVG(wo.throughput_uph) - rb.throughput_target, 1)    AS throughput_gap,
    ROUND(AVG(wo.defect_rate_pct) - rb.defect_rate_target, 2)  AS defect_gap,
    CASE
        WHEN AVG(wo.throughput_uph) < rb.throughput_target THEN 'BELOW BENCHMARK'
        ELSE 'ON TARGET'
    END                                                         AS throughput_status
FROM warehouse_operations wo
LEFT JOIN region_benchmarks rb ON wo.region = rb.region
GROUP BY wo.region, rb.throughput_target, rb.defect_rate_target
ORDER BY avg_throughput ASC;


-- ── KPIs by Shift ─────────────────────────────────────────────
SELECT
    shift,
    COUNT(*)                                            AS total_orders,
    ROUND(AVG(throughput_uph), 1)                       AS avg_throughput,
    ROUND(AVG(dock_delay_hrs), 2)                       AS avg_dock_delay,
    ROUND(AVG(defect_rate_pct), 2)                      AS avg_defect_rate,
    ROUND(CAST(SUM(CAST(sla_met AS INT)) AS FLOAT)
          / COUNT(*) * 100, 1)                          AS sla_compliance_pct,
    ROUND(AVG(cost_per_unit), 2)                        AS avg_cost_per_unit
FROM warehouse_operations
GROUP BY shift
ORDER BY shift;


-- ── Monthly Trend ─────────────────────────────────────────────
SELECT
    FORMAT(order_date, 'yyyy-MM')                       AS month,
    COUNT(*)                                            AS total_orders,
    ROUND(AVG(throughput_uph), 1)                       AS avg_throughput,
    ROUND(AVG(dock_delay_hrs), 2)                       AS avg_dock_delay,
    ROUND(AVG(defect_rate_pct), 2)                      AS avg_defect_rate,
    ROUND(CAST(SUM(CAST(sla_met AS INT)) AS FLOAT)
          / COUNT(*) * 100, 1)                          AS sla_compliance_pct,
    ROUND(SUM(cost_per_unit * units_processed), 0)      AS total_cost
FROM warehouse_operations
GROUP BY FORMAT(order_date, 'yyyy-MM')
ORDER BY month;


-- ── Dock Delay Distribution ───────────────────────────────────
SELECT
    CASE
        WHEN dock_delay_hrs < 1    THEN '< 1 hr'
        WHEN dock_delay_hrs < 2    THEN '1–2 hrs'
        WHEN dock_delay_hrs < 4    THEN '2–4 hrs'
        ELSE '> 4 hrs'
    END                                                 AS delay_bucket,
    COUNT(*)                                            AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct_of_total
FROM warehouse_operations
GROUP BY
    CASE
        WHEN dock_delay_hrs < 1    THEN '< 1 hr'
        WHEN dock_delay_hrs < 2    THEN '1–2 hrs'
        WHEN dock_delay_hrs < 4    THEN '2–4 hrs'
        ELSE '> 4 hrs'
    END
ORDER BY MIN(dock_delay_hrs);


-- ── Top 10 Costliest Days ─────────────────────────────────────
SELECT TOP 10
    order_date,
    region,
    shift,
    ROUND(SUM(cost_per_unit * units_processed), 0)      AS total_daily_cost,
    ROUND(AVG(defect_rate_pct), 2)                      AS avg_defect_rate,
    ROUND(AVG(dock_delay_hrs), 2)                       AS avg_dock_delay
FROM warehouse_operations
GROUP BY order_date, region, shift
ORDER BY total_daily_cost DESC;
