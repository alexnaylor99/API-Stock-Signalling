import requests
from datetime import datetime, timedelta
from time import sleep  # <-- Added this line here
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 2.2 set up global variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
IFTTT_WEBHOOK_KEY = os.getenv("IFTTT_WEBHOOK_KEY")
IFTTT_URL = f"https://maker.ifttt.com/trigger/stock_price_drop/with/key/{IFTTT_WEBHOOK_KEY}"
STOCKS = ["TSLA", "AAPL", "MSFT", "GOOGL", "NKE"]  # Stock symbols for Tesla, Apple, Microsoft, Google, and Nike.
PRICE_DROP_LIMIT = 0.25

# 2.3 define function to get stock price:

def get_stock_price(stock_symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_DAILY"
    params = {
        "function": function,
        "symbol": stock_symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(base_url, params=params).json()
    print(response)  # <-- Added this line to debug
    return response["Time Series (Daily)"]

# 2.4 Define Function to Calculate the 7 Day Average:

def calculate_seven_day_average(price_data):
    last_seven_days = sorted(price_data.keys())[-7:]
    return sum(float(price_data[day]["4. close"]) for day in last_seven_days) / 7

# 2.5 Define a Function to Send Notification:

def send_notification(stock, current_price, seven_day_avg):
    data = {
        "value1": stock,
        "value2": f"£{current_price}",
        "value3": f"£{seven_day_avg:.2f}"
    }
    requests.post(IFTTT_URL, data=data)

# 2.6. Main Function to Monitor and Notify:

def monitor_and_notify():
    for stock in STOCKS:
        price_data = get_stock_price(stock)
        current_price = float(price_data[sorted(price_data.keys())[-1]]["4. close"])
        seven_day_avg = calculate_seven_day_average(price_data)

        if current_price <= seven_day_avg - PRICE_DROP_LIMIT or current_price < seven_day_avg:
            send_notification(stock, current_price, seven_day_avg)

# 2.7. Main Execution:

if __name__ == "__main__":
    while True:  # This creates an infinite loop
        monitor_and_notify()
        sleep(300)  # Sleep for 5 minutes
