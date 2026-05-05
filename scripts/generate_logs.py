# ── SentinelX Log Generator ────────────────────────────────
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import TOTAL_LOGS, RAW_LOGS_PATH, HIGH_RISK_COUNTRIES

fake = Faker()

# ── Define users and IPs ───────────────────────────────────
USERS = ["admin", "root", "john.doe", "jane.smith", "service_acc", "guest", "backup_user"]

IP_POOL = [
    {"ip": "192.168.1.10", "country": "Egypt",       "flag": "🇪🇬", "safe": True},
    {"ip": "10.0.0.5",     "country": "Egypt",       "flag": "🇪🇬", "safe": True},
    {"ip": "172.16.0.8",   "country": "Egypt",       "flag": "🇪🇬", "safe": True},
    {"ip": "45.33.32.156", "country": "USA",         "flag": "🇺🇸", "safe": True},
    {"ip": "185.23.45.2",  "country": "Russia",      "flag": "🇷🇺", "safe": False},
    {"ip": "91.108.4.200", "country": "China",       "flag": "🇨🇳", "safe": False},
    {"ip": "198.51.100.5", "country": "Iran",        "flag": "🇮🇷", "safe": False},
    {"ip": "203.0.113.77", "country": "North Korea", "flag": "🇰🇵", "safe": False},
    {"ip": "194.165.16.11","country": "Belarus",     "flag": "🇧🇾", "safe": False},
]

EVENT_TYPES = ["login", "SSH", "API", "VPN", "RDP"]

# ── Generate logs ──────────────────────────────────────────
def generate_logs():
    logs = []
    base_time = datetime(2026, 5, 5, 6, 0, 0)

    print(f"[*] Generating {TOTAL_LOGS} log entries...")

    for i in range(TOTAL_LOGS):
        ip_obj   = random.choice(IP_POOL)
        user     = random.choice(USERS)
        event    = random.choice(EVENT_TYPES)

        # Unsafe IPs fail more often
        fail_chance = 0.80 if not ip_obj["safe"] else 0.10
        status   = "FAILED" if random.random() < fail_chance else "SUCCESS"

        timestamp = base_time + timedelta(seconds=i * 170 + random.randint(0, 60))

        logs.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "user":      user,
            "ip":        ip_obj["ip"],
            "country":   ip_obj["country"],
            "flag":      ip_obj["flag"],
            "status":    status,
            "event_type": event,
            "safe":      ip_obj["safe"],
        })

    df = pd.DataFrame(logs)
    os.makedirs("data", exist_ok=True)
    df.to_csv(RAW_LOGS_PATH, index=False)
    print(f"[✓] Saved {len(df)} logs to {RAW_LOGS_PATH}")
    return df

if __name__ == "__main__":
    generate_logs()