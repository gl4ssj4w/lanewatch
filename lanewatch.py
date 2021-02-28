#!/usr/bin/env python3
"""lanewatch: log posted spot rates for a few truckload lanes to data/rates.csv."""
import csv, datetime, os, subprocess, sys, time
import requests

RATE_SOURCE = os.environ.get("RATE_SOURCE", "")   # JSON endpoint, set in the environment
LANES = "lanes.csv"
OUT = "data/rates.csv"


def log(msg):
    print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def net_check(retries=3):
    """The Pi's Wi-Fi drops now and then. Wait for the link before scraping."""
    for _ in range(retries):
        out = subprocess.run(["iw", "dev", "wlan0", "link"], capture_output=True, text=True).stdout
        if out.startswith("Connected to "):
            bssid = out.split()[2]
            signal = next((l.split(":")[1].strip() for l in out.splitlines() if "signal:" in l), "?")
            log(f"net check: wlan0 connected to {bssid}, signal {signal}")
            return True
        log("net check: wlan0 not connected, retry in 60s")
        time.sleep(60)
    return False


def main():
    if not net_check():
        log("giving up: no network")
        sys.exit(1)
    if not RATE_SOURCE:
        log("RATE_SOURCE not set")
        sys.exit(1)
    os.makedirs("data", exist_ok=True)
    with open(LANES) as f, open(OUT, "a", newline="") as out:
        w = csv.writer(out)
        for lane in csv.DictReader(f):
            r = requests.get(RATE_SOURCE, params=lane, timeout=20)
            rate = r.json().get("rate_per_mile")
            w.writerow([datetime.date.today(), lane["origin"], lane["destination"], lane["equipment"], rate])
            log(f"{lane['origin']} -> {lane['destination']} ({lane['equipment']}): {rate}")
            time.sleep(2)
    log("done")


if __name__ == "__main__":
    main()
