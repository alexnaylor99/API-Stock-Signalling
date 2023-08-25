import os
from time import sleep
from dotenv import load_dotenv
from price_alert_utils import fetch_price_and_avg, notify_ifttt

load_dotenv()

IEX_API_KEY = os.getenv('IEX_API_KEY')
IFTTT_WEBHOOK_KEY = os.getenv('IFTTT_WEBHOOK_KEY')
SYMBOLS = ['TSLA', 'AAPL', 'MSFT', 'GOOGL', 'NKE']
BASE_IEX_URL = "https://cloud.iexapis.com/stable"

def main():
    while True:
        for symbol in SYMBOLS:
            today_price, avg_7_day = fetch_price_and_avg(symbol, BASE_IEX_URL, IEX_API_KEY)    
            if today_price is None or avg_7_day is None:
                continue
            if today_price < avg_7_day or (avg_7_day - today_price) >= 0.25:
                notify_ifttt(IFTTT_WEBHOOK_KEY, "price_alert", symbol, str(today_price), str(avg_7_day))
        sleep(900)

if __name__ == "__main__":
    main()