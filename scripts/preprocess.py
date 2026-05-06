# ── SentinelX Preprocessor ─────────────────────────────────
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import RAW_LOGS_PATH, PROCESSED_LOGS_PATH, WORK_HOURS_START, WORK_HOURS_END

def preprocess_logs(df):
    print("[*] Preprocessing logs...")

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Extract useful time columns
    df["hour"]    = df["timestamp"].dt.hour
    df["date"]    = df["timestamp"].dt.date
    df["weekday"] = df["timestamp"].dt.day_name()

    # Flag off-hours activity
    df["off_hours"] = ~df["hour"].between(WORK_HOURS_START, WORK_HOURS_END)

    # Count failed attempts per IP
    fail_counts = (
        df[df["status"] == "FAILED"]
        .groupby("ip")
        .size()
        .reset_index(name="failed_attempts")
    )
    df = df.merge(fail_counts, on="ip", how="left")
    df["failed_attempts"] = df["failed_attempts"].fillna(0).astype(int)

    # Count unique IPs per user
    ip_per_user = (
        df.groupby("user")["ip"]
        .nunique()
        .reset_index(name="unique_ips")
    )
    df = df.merge(ip_per_user, on="user", how="left")

    # Save processed file
    os.makedirs("data", exist_ok=True)
    df.to_csv(PROCESSED_LOGS_PATH, index=False)

    print(f"[✓] Processed {len(df)} logs")

    return df