
Q2 = """
WITH windows AS (
  SELECT * FROM (VALUES
    ('Suez Canal',           DATE '2023-01-01', DATE '2023-10-31'),
    ('Bab el-Mandeb Strait', DATE '2023-01-01', DATE '2023-10-31'),
    ('Cape of Good Hope',    DATE '2023-01-01', DATE '2023-10-31'),
    ('Strait of Hormuz',     DATE '2025-01-01', DATE '2026-01-31')
  ) AS t(portname, base_start, base_end)
),
latest AS (SELECT MAX(date) AS d FROM daily),
long AS (
  UNPIVOT daily ON n_container, n_dry_bulk, n_general_cargo, n_roro, n_tanker
  INTO NAME ship_type VALUE transits
)
SELECT w.portname, REPLACE(l.ship_type, 'n_', '') AS ship_type,
       ROUND(AVG(CASE WHEN l.date BETWEEN w.base_start AND w.base_end THEN l.transits END), 1) AS baseline_avg,
       ROUND(AVG(CASE WHEN l.date >= (SELECT d FROM latest) - INTERVAL 27 DAY THEN l.transits END), 1) AS last_28d_avg,
       ROUND(100 * (AVG(CASE WHEN l.date >= (SELECT d FROM latest) - INTERVAL 27 DAY THEN l.transits END)
             / NULLIF(AVG(CASE WHEN l.date BETWEEN w.base_start AND w.base_end THEN l.transits END), 0) - 1), 1) AS pct_change
FROM windows w JOIN long l ON l.portname = w.portname
GROUP BY w.portname, l.ship_type ORDER BY w.portname, l.ship_type
"""
con.sql(Q2).df()
