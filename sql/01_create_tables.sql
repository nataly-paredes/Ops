-- ============================================================
-- 01_create_tables.sql
-- Warehouse Operations schema setup
-- ============================================================

CREATE TABLE warehouse_operations (
    order_id                  VARCHAR(20)    PRIMARY KEY,
    order_date                DATE           NOT NULL,
    month                     VARCHAR(7),
    region                    VARCHAR(60)    NOT NULL,
    shift                     VARCHAR(10)    NOT NULL,
    throughput_uph            DECIMAL(8,2),
    dock_delay_hrs            DECIMAL(8,2),
    defect_rate_pct           DECIMAL(6,2),
    inventory_accuracy_pct    DECIMAL(6,2),
    sla_hours                 DECIMAL(8,2),
    sla_met                   BIT,
    cost_per_unit             DECIMAL(8,2),
    units_processed           INT
);

-- Regional benchmark reference table
CREATE TABLE region_benchmarks (
    region          VARCHAR(60) PRIMARY KEY,
    throughput_target   DECIMAL(8,2) DEFAULT 120.0,
    dock_delay_target   DECIMAL(8,2) DEFAULT 1.0,
    defect_rate_target  DECIMAL(6,2) DEFAULT 2.0,
    sla_target_pct      DECIMAL(6,2) DEFAULT 95.0,
    inv_accuracy_target DECIMAL(6,2) DEFAULT 98.0
);

INSERT INTO region_benchmarks (region) VALUES
    ('Region 1 - Northeast'),
    ('Region 2 - Southeast'),
    ('Region 3 - Mid-Atlantic'),
    ('Region 4 - Midwest'),
    ('Region 5 - South');
