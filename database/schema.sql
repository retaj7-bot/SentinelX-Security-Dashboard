-- ── SentinelX Database Schema ──────────────────────────────

-- Main logs table
CREATE TABLE IF NOT EXISTS logs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp     DATETIME,
    user          TEXT,
    ip            TEXT,
    country       TEXT,
    flag          TEXT,
    status        TEXT,
    event_type    TEXT,
    safe          BOOLEAN,
    hour          INTEGER,
    date          DATE,
    weekday       TEXT,
    off_hours     BOOLEAN,
    failed_attempts INTEGER,
    unique_ips    INTEGER
);

-- Threats table
CREATE TABLE IF NOT EXISTS threats (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    threat_type   TEXT,
    severity      TEXT,
    detail        TEXT,
    ip            TEXT
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_ip      ON logs(ip);
CREATE INDEX IF NOT EXISTS idx_status  ON logs(status);
CREATE INDEX IF NOT EXISTS idx_country ON logs(country);
CREATE INDEX IF NOT EXISTS idx_user    ON logs(user);
CREATE INDEX IF NOT EXISTS idx_time    ON logs(timestamp);