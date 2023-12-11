import requests
import time
import os
import csv
from datetime import datetime

def get_tether_market_cap():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd&include_market_cap=true"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return int(data['tether']['usd_market_cap'])
    except requests.RequestException as e:
        print(f"Error fetching market cap: {e}")
        return None

def get_filename(base, date):
    return os.path.join("data", f"{base}_{date}.csv")

def write_to_csv(filename, data, mode='a'):
    with open(filename, mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def ensure_directory():
    if not os.path.exists("data"):
        os.makedirs("data")

def main():
    ensure_directory()
    last_market_cap = None
    last_date = datetime.now().strftime("%Y-%m-%d")

    while True:
        current_date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        market_cap = get_tether_market_cap()
        
        if market_cap is not None:
            if current_date != last_date:
                last_market_cap = None
                last_date = current_date

            base_filename = "tether_market_cap"
            changes_base_filename = "tether_market_cap_changes"

            filename = get_filename(base_filename, current_date)
            changes_filename = get_filename(changes_base_filename, current_date)

            # Check for new day to write headers
            if last_market_cap is None:
                write_to_csv(filename, ["Timestamp", "Market Cap"], 'w')
                write_to_csv(changes_filename, ["Timestamp", "Old Market Cap", "New Market Cap", "Difference"], 'w')

            # Writing the current market cap to CSV
            write_to_csv(filename, [timestamp, market_cap])

            if last_market_cap is not None and market_cap != last_market_cap:
                difference = market_cap - last_market_cap
                change_log = [timestamp, last_market_cap, market_cap, difference]
                write_to_csv(changes_filename, change_log)

            last_market_cap = market_cap

        time.sleep(300)

if __name__ == "__main__":
    main()
