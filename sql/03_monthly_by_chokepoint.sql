-- Monthly average transits per day for Suez and Cape of Good Hope. Source: UN Global Platform; IMF PortWatch.
SELECT date_trunc('month', date) AS month, portname, ROUND(AVG(n_total), 1) AS avg_per_day
FROM daily
WHERE portname IN ('Suez Canal', 'Cape of Good Hope') AND date >= DATE '2022-01-01'
GROUP BY 1, 2 ORDER BY 1, 2
