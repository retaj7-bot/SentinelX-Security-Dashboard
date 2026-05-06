# ── SentinelX Database Loader ──────────────────────────────
import pandas as pd
import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import PROCESSED_LOGS_PATH, DB_PATH

def load_database():
    print("[*] Connecting to database...")
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute schema
    print("[*] Creating tables...")
    with open("database/schema.sql", "r") as f:
        cursor.executescript(f.read())

    # Load processed logs
    print("[*] Loading logs into database...")
    df_logs = pd.read_csv(PROCESSED_LOGS_PATH)
    df_logs.to_sql("logs", conn, if_exists="replace", index=False)
    print(f"[✓] Inserted {len(df_logs)} log entries")

    # Load threats
    print("[*] Loading threats into database...")
    df_threats = pd.read_csv("data/threats.csv")
    df_threats.to_sql("threats", conn, if_exists="replace", index=False)
    print(f"[✓] Inserted {len(df_threats)} threats")

    # Run a quick test query
    print("\n── Quick Database Test ───────────────────")
    cursor.execute("SELECT status, COUNT(*) FROM logs GROUP BY status")
    for row in cursor.fetchall():
        print(f"    {row[0]}: {row[1]} events")

    cursor.execute("SELECT severity, COUNT(*) FROM threats GROUP BY severity")
    print("\n── Threats in DB ─────────────────────────")
    for row in cursor.fetchall():
        print(f"    {row[0]}: {row[1]} threats")
    print("──────────────────────────────────────────")

    conn.commit()
    conn.close()
    print("\n[✓] Database ready at database/sentinelx.db\n")

if __name__ == "__main__":
    load_database()