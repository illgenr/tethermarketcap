import requests
import time
import os
from datetime import datetime

def get_tether_market_cap():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd&include_market_cap=true"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['tether']['usd_market_cap']
    except requests.RequestException as e:
        print(f"Error fetching market cap: {e}")
        return None

def get_filename(base, date):
    return os.path.join("data", f"{base}_{date}.txt")

def write_to_file(filename, content, mode='w'):
    with open(filename, mode) as file:
        file.write(content)

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

            write_to_file(filename, f"{timestamp}: {market_cap}\n", 'a')

            if last_market_cap is not None and market_cap != last_market_cap:
                difference = market_cap - last_market_cap
                change_log = f"{timestamp}: {last_market_cap} to {market_cap} Change: {difference}\n"
                write_to_file(changes_filename, change_log, 'a')

            last_market_cap = market_cap

            #wait 30 minutes
        time.sleep(1800)

if __name__ == "__main__":
    main()
