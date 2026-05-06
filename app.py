# ── SentinelX Flask Dashboard ──────────────────────────────
from flask import Flask, render_template
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Load data
    logs_df     = pd.read_csv("data/processed_logs.csv")
    threats_df  = pd.read_csv("data/threats.csv")

    # Stats
    total    = len(logs_df)
    failed   = len(logs_df[logs_df["status"] == "FAILED"])
    success  = len(logs_df[logs_df["status"] == "SUCCESS"])
    off_hours = len(logs_df[logs_df["off_hours"] == True])
    fail_pct = round(failed / total * 100)

    stats = {
        "total":     total,
        "failed":    failed,
        "success":   success,
        "threats":   len(threats_df),
        "off_hours": off_hours,
        "fail_pct":  fail_pct,
    }

    # Hour chart data
    logs_df["hour"] = pd.to_datetime(logs_df["timestamp"]).dt.hour
    hour_data = (
        logs_df[logs_df["status"] == "FAILED"]
        .groupby("hour").size()
        .reset_index(name="count")
        .rename(columns={"hour": "hour"})
        .to_dict(orient="records")
    )

    # Top IPs chart data
    ip_data = (
        logs_df[logs_df["status"] == "FAILED"]
        .groupby("ip").size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(6)
        .rename(columns={"ip": "ip"})
        .to_dict(orient="records")
    )

    # Threats list
    threats = threats_df.to_dict(orient="records")

    # Recent logs
    logs = logs_df.head(50).to_dict(orient="records")

    current_time = datetime.now().strftime("%H:%M:%S")

    return render_template("dashboard.html",
        stats=stats,
        hour_data=hour_data,
        ip_data=ip_data,
        threats=threats,
        logs=logs,
        current_time=current_time,
    )

if __name__ == "__main__":
    app.run(debug=True)