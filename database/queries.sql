-- ── SentinelX Useful Queries ───────────────────────────────

-- Total events
SELECT COUNT(*) AS total_events FROM logs;

-- Failed vs success count
SELECT status, COUNT(*) AS count
FROM logs
GROUP BY status;

-- Top 10 most aggressive IPs
SELECT ip, country, COUNT(*) AS failed_attempts
FROM logs
WHERE status = 'FAILED'
GROUP BY ip
ORDER BY failed_attempts DESC
LIMIT 10;

-- Attacks by country
SELECT country, flag, COUNT(*) AS attempts
FROM logs
WHERE status = 'FAILED'
GROUP BY country
ORDER BY attempts DESC;

-- Off-hours login attempts
SELECT timestamp, user, ip, country, status
FROM logs
WHERE off_hours = 1
ORDER BY timestamp;

-- Most targeted users
SELECT user, COUNT(*) AS failed_attempts
FROM logs
WHERE status = 'FAILED'
GROUP BY user
ORDER BY failed_attempts DESC;

-- All critical threats
SELECT * FROM threats
WHERE severity = 'CRITICAL';

-- Attacks per hour of day
SELECT hour, COUNT(*) AS attempts
FROM logs
WHERE status = 'FAILED'
GROUP BY hour
ORDER BY hour;