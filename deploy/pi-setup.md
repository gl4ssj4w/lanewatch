# Pi setup

1. Flash Raspberry Pi OS Lite, set hostname `lanewatch`, enable SSH.
2. Join home Wi-Fi with `raspi-config` (Wi-Fi drops sometimes, so the script checks the link first).
3. `git clone` this repo into `~/lanewatch` and install requirements.
4. cron: `15 6 * * * cd ~/lanewatch && /usr/bin/python3 lanewatch.py >> logs/scraper.log 2>&1`
