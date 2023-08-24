import requests
import time

# API key with IEX Cloud
api_key = "pk_c2257f70a6584faca4bb653bd4618478"

# Stocks to monitor
stocks = ["TSLA", "AAPL", "MSFT", "GOOGL", "NKE"]

# IFTTT Webhook URL 
IFTTT_webhook_url = "https://maker.ifttt.com/trigger/stock_price_falls/with/key/hKArh7xueLrGZEGnVP-IB4nYOdWZ3bR-hiMDYmTt283"

# Create a dictionary to store previous prices for each week
previous_prices = {}

# Function to fetch stock prices
def get_stock_price(symbol):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}"
    response = requests.get(url)
    data = response.json()
    return float(data["latestPrice"]) 

"""
# Function to fetch 7-day average price
def get_7day_average(symbol):
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}"
    response = requests.get(url)
    data = response.json()
    prices = [float(entry["close"]) for entry in data["values"]]
    average = sum(prices) / len(prices)
    return average
"""


# Function to send IFTTT notification
def send_notification(stock_symbol, price):
    payload = {
        "value1": stock_symbol,
        "value2": str(price)
    }
    requests.post(IFTTT_webhook_url, json=payload)

# Main monitoring loop
while True:
    print("Monitoring stock prices...")

    for stock_symbol in stocks:
        current_price = get_stock_price(stock_symbol)
    
        if stock_symbol in previous_prices:
            price_change = previous_prices[stock_symbol] - current_price
            
            if price_change >= 0.25: 
                send_notification(stock_symbol, current_price)
                print(f"{stock_symbol} price fell by £0.25 or more. Sending notification.")
            else:
                print(f"{stock_symbol} price change: £{price_change: .2f}")
        
        previous_prices[stock_symbol] = current_price
    

# Check every 1 minute 
time.sleep(60)

