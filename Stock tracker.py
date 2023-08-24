

import requests
import time
from dotenv import load_dotenv

load_dotenv() #Load environment from hidekey.env file

#IEX API-Key
api_key = "pk_d9106159d4b94a68992bab8dc9d9b802"

# IFTTT Webhooks key
ifttt_webhook_key = "bbeU9zbIZ3d0Q1AwZqlsh7"
ifttt_webhook_url = "https://maker.ifttt.com/trigger/twentyfive_drop/with/key/bbeU9zbIZ3d0Q1AwZqlsh7"

# Stock symbols to monitor
assets = ["AAPL", "GOOGL", "TSLA", "NKE", "MSFT"]  
price_decline = -0.25  # GBP
seven_day_average = 7

# Dictionary for previous price
previous_prices = {}

# Function to fetch stock data from data provider
def get_asset_data(symbol):
    url=f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}"
    response = requests.get(url).json()
    data = response
    return data['latestPrice']



# Function to send IFTTT notification
def send_ifttt_notification(assets, price):

    payload = {
        "value1": assets,
        "value2": str(price)
    }
    response = requests.post(ifttt_webhook_url, json=payload)

send_ifttt_notification

# Main scanning loop
while True:
    print("Scanning stock prices...")
 
    for stock_symbol in assets:
        current_price = get_asset_data(stock_symbol)
   
        if stock_symbol in previous_prices:
            price_change = previous_prices[stock_symbol] - current_price
           
            if price_change >= 0.25:
                send_ifttt_notification(stock_symbol, current_price)
                print(f"{stock_symbol} price fell by £0.25 or more. Sending notification.")
            else:
                print(f"{stock_symbol} price change: £{price_change: .2f}")
       
        previous_prices[stock_symbol] = current_price
   
 
# Check every 1 minute
time.sleep(60)
   

 
 