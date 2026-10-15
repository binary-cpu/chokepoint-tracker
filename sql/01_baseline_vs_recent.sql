-- Baseline vs last 28 days, daily transits. Source: UN Global Platform; IMF PortWatch.
WITH windows AS (
  SELECT * FROM (VALUES
    ('Suez Canal',           DATE '2023-01-01', DATE '2023-10-31'),
    ('Bab el-Mandeb Strait', DATE '2023-01-01', DATE '2023-10-31'),
    ('Cape of Good Hope',    DATE '2023-01-01', DATE '2023-10-31'),
    ('Strait of Hormuz',     DATE '2025-01-01', DATE '2026-01-31')
  ) AS t(portname, base_start, base_end)
),
latest AS (SELECT MAX(date) AS d FROM daily)
SELECT w.portname,
       ROUND(AVG(CASE WHEN d.date BETWEEN w.base_start AND w.base_end THEN d.n_total END), 1) AS baseline_avg_per_day,
       ROUND(AVG(CASE WHEN d.date >= (SELECT d FROM latest) - INTERVAL 27 DAY THEN d.n_total END), 1) AS last_28d_avg_per_day,
       ROUND(100 * (AVG(CASE WHEN d.date >= (SELECT d FROM latest) - INTERVAL 27 DAY THEN d.n_total END)
                  / AVG(CASE WHEN d.date BETWEEN w.base_start AND w.base_end THEN d.n_total END) - 1), 1) AS pct_change
FROM windows w JOIN daily d ON d.portname = w.portname
GROUP BY w.portname ORDER BY w.portname
