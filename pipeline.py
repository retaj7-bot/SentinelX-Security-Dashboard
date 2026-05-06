# ── SentinelX Pipeline ─────────────────────────────────────
import pandas as pd
from scripts.generate_logs import generate_logs
from scripts.preprocess import preprocess_logs
from scripts.detect_threats import detect
from scripts.load_database import load_database

def run_pipeline():
    print("\n🔄 Step 1 — Generating logs...")
    generate_logs()

    print("\n🧹 Step 2 — Preprocessing logs...")
    df = pd.read_csv("data/raw_logs.csv")
    preprocess_logs(df)

    print("\n🚨 Step 3 — Detecting threats...")
    df2 = pd.read_csv("data/processed_logs.csv")
    detect()

    print("\n💾 Step 4 — Storing in database...")
    load_database()

    print("\n✅ Pipeline completed successfully!")
    print("   → 500 logs generated")
    print("   → threats detected and saved")
    print("   → database updated")

if __name__ == "__main__":
    run_pipeline()