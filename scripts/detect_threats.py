# ── SentinelX Threat Detection Engine ──────────────────────
import pandas as pd
import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import (PROCESSED_LOGS_PATH, BRUTE_FORCE_THRESHOLD,
                             HIGH_RISK_COUNTRIES, WORK_HOURS_START, WORK_HOURS_END)

threats = []

def log_threat(threat_type, severity, detail, ip="N/A"):
    threats.append({
        "threat_type": threat_type,
        "severity":    severity,
        "detail":      detail,
        "ip":          ip,
    })
    color = {
        "CRITICAL": Fore.RED,
        "HIGH":     Fore.YELLOW,
        "MEDIUM":   Fore.CYAN,
        "LOW":      Fore.GREEN,
    }.get(severity, Fore.WHITE)
    print(f"{color}[{severity}] {threat_type} — {detail}{Style.RESET_ALL}")

def detect():
    print(f"\n{Fore.CYAN}══ SentinelX Threat Detection Engine ══{Style.RESET_ALL}\n")

    df = pd.read_csv(PROCESSED_LOGS_PATH)
    failed = df[df["status"] == "FAILED"]

    # ── Rule 1: Brute Force ────────────────────────────────
    print("[*] Checking for brute force attacks...")
    ip_fails = failed.groupby("ip").size()
    for ip, count in ip_fails.items():
        if count >= BRUTE_FORCE_THRESHOLD:
            country = df[df["ip"] == ip]["country"].iloc[0]
            severity = "CRITICAL" if count >= 10 else "HIGH"
            log_threat("BRUTE FORCE", severity,
                       f"{count} failed logins from {ip} ({country})", ip)

    # ── Rule 2: Geo Anomaly ────────────────────────────────
    print("\n[*] Checking for geo anomalies...")
    risky = failed[failed["country"].isin(HIGH_RISK_COUNTRIES)]
    risky_ips = risky.groupby(["ip","country"]).size()
    for (ip, country), count in risky_ips.items():
        log_threat("GEO ANOMALY", "HIGH",
                   f"{count} failed attempts from high-risk country: {country}", ip)

    # ── Rule 3: Off-hours access ───────────────────────────
    print("\n[*] Checking for off-hours access...")
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    off = df[~df["hour"].between(WORK_HOURS_START, WORK_HOURS_END)]
    if len(off) > 0:
        log_threat("OFF-HOURS ACCESS", "MEDIUM",
                   f"{len(off)} login attempts outside work hours ({WORK_HOURS_START}:00–{WORK_HOURS_END}:00)")

    # ── Rule 4: Credential Stuffing ───────────────────────
    print("\n[*] Checking for credential stuffing...")
    ip_per_user = df.groupby("user")["ip"].nunique()
    for user, count in ip_per_user.items():
        if count >= 4:
            log_threat("CREDENTIAL STUFFING", "HIGH",
                       f'User "{user}" accessed from {count} different IPs')

    # ── Rule 5: Privilege account targeting ───────────────
    print("\n[*] Checking privileged account attacks...")
    priv_accounts = ["admin", "root", "service_acc"]
    priv_fails = failed[failed["user"].isin(priv_accounts)]
    if len(priv_fails) > 10:
        log_threat("PRIVILEGED ACCOUNT ATTACK", "CRITICAL",
                   f"{len(priv_fails)} failed attempts on privileged accounts")

    # ── Summary ────────────────────────────────────────────
    print(f"\n{Fore.CYAN}══ Detection Complete ══{Style.RESET_ALL}")
    print(f"    Total threats found: {Fore.RED}{len(threats)}{Style.RESET_ALL}")

    counts = pd.Series([t["severity"] for t in threats]).value_counts()
    for severity, count in counts.items():
        print(f"    {severity}: {count}")

    # Save threats to CSV
    threat_df = pd.DataFrame(threats)
    threat_df.to_csv("data/threats.csv", index=False)
    print(f"\n{Fore.GREEN}[✓] Threats saved to data/threats.csv{Style.RESET_ALL}\n")

if __name__ == "__main__":
    detect()