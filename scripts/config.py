# ── SentinelX Configuration File ──────────────────────────
# All settings in one place — change these anytime

# How many fake log entries to generate
TOTAL_LOGS = 500

# Brute force threshold (failed attempts from same IP)
BRUTE_FORCE_THRESHOLD = 5

# Off-hours definition (logins outside this range are suspicious)
WORK_HOURS_START = 7
WORK_HOURS_END = 22

# High-risk countries
HIGH_RISK_COUNTRIES = ["Russia", "China", "Iran", "North Korea", "Belarus"]

# Output file paths
RAW_LOGS_PATH = "data/raw_logs.csv"
PROCESSED_LOGS_PATH = "data/processed_logs.csv"

# Database
DB_PATH = "database/sentinelx.db"