#!/usr/bin/env python3
"""lanewatch: log posted spot rates for a few truckload lanes to data/rates.csv."""
import csv, datetime, os, sys, time
import requests

RATE_SOURCE = os.environ.get("RATE_SOURCE", "")   # JSON endpoint, set in the environment
LANES = "lanes.csv"
OUT = "data/rates.csv"


def log(msg):
    print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)



def main():
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
