# lanewatch

Tracks posted spot rates on a handful of truckload lanes and writes them to a CSV so I can
see how they move week to week.

## Setup

```
pip install -r requirements.txt
cp lanes.example.csv lanes.csv
python3 lanewatch.py
```

Set `RATE_SOURCE` to the JSON endpoint you're pulling from. Be polite: one request per lane, once a day.

## Running it unattended

Runs on a Pi 4 from cron (see `deploy/pi-setup.md`). Logs go to `logs/scraper.log`.
